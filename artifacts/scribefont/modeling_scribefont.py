"""ScribeFont neural architecture: 2D Vision Calligrapher Style Encoder + Cross-Attention Bézier Glyph Decoder."""
from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import PreTrainedConfig, PreTrainedModel


class ScribeFontConfig(PreTrainedConfig):
    model_type = "scribefont"

    def __init__(
        self,
        vocab_size: int = 62,
        num_writers: int = 12,
        num_points: int = 16,
        style_dim: int = 128,
        hidden_dim: int = 256,
        num_layers: int = 4,
        num_heads: int = 8,
        dropout: float = 0.05,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.num_writers = num_writers
        self.num_points = num_points
        self.style_dim = style_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.dropout = dropout


class ConvResidualBlock(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.norm1 = nn.GroupNorm(4, channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.norm2 = nn.GroupNorm(4, channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = F.gelu(self.norm1(self.conv1(x)))
        h = self.norm2(self.conv2(h))
        return F.gelu(x + h)


class ScribeFontForGeneration(PreTrainedModel):
    config_class = ScribeFontConfig

    def __init__(self, config: ScribeFontConfig) -> None:
        super().__init__(config)
        self.config = config

        # 1. 2D Reference Sheet Vision Encoder (4 reference glyphs x 16x16 + 1 target cell x 16x16)
        self.ref_conv_stem = nn.Sequential(
            nn.Conv2d(4, 64, kernel_size=3, padding=1),
            nn.GroupNorm(8, 64),
            nn.GELU(),
            ConvResidualBlock(64),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),  # -> [B, 128, 8, 8]
            nn.GroupNorm(8, 128),
            nn.GELU(),
            ConvResidualBlock(128),
        )
        self.target_conv_stem = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.GroupNorm(4, 32),
            nn.GELU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),   # -> [B, 64, 8, 8]
            nn.GroupNorm(8, 64),
            nn.GELU(),
        )

        # Fuse visual patch features + 8 biometric summary features into 128-d Calligrapher Style Vector
        self.style_projector = nn.Sequential(
            nn.Linear(128 * 4 + 64 + 8, config.hidden_dim),
            nn.LayerNorm(config.hidden_dim),
            nn.GELU(),
            nn.Linear(config.hidden_dim, config.style_dim),
            nn.LayerNorm(config.style_dim),
            nn.GELU(),
        )

        # Predict 8 normalized biometric style dimensions directly from visual + summary features
        self.style_reg_head = nn.Sequential(
            nn.Linear(config.style_dim, config.style_dim),
            nn.GELU(),
            nn.Linear(config.style_dim, 8),
            nn.Sigmoid(),
        )

        # Writer archetype identification head (12 writer styles)
        self.writer_head = nn.Linear(config.style_dim, config.num_writers)

        # Missing / blank / smudged glyph cell detector head (calibrated p_missing)
        self.missing_head = nn.Sequential(
            nn.Linear(64 + config.style_dim, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Linear(128, 1),
        )

        # 2. Unicode Character & Point-Index Transformer Decoder
        self.char_emb = nn.Embedding(config.vocab_size, config.hidden_dim)
        self.point_emb = nn.Embedding(config.num_points, config.hidden_dim)
        self.base_coord_proj = nn.Linear(2, config.hidden_dim)
        self.style_to_dec = nn.Linear(config.style_dim + 8, config.hidden_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_dim,
            nhead=config.num_heads,
            dim_feedforward=config.hidden_dim * 2,
            dropout=config.dropout,
            activation="gelu",
            batch_first=True,
        )
        self.glyph_transformer = nn.TransformerEncoder(encoder_layer, num_layers=config.num_layers)

        # Predicts residual coordinate adjustments [B, 16, 2] around canonical skeleton
        self.contour_head = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.GELU(),
            nn.Linear(config.hidden_dim // 2, 2),
        )

        # Predicts 5 normalized glyph metrics: [advance_width, lsb, slant_deg, stroke_width, kern_av]
        self.metrics_head = nn.Sequential(
            nn.Linear(config.hidden_dim + config.style_dim + 8, 128),
            nn.GELU(),
            nn.Linear(128, 5),
            nn.Sigmoid(),
        )

        self.post_init()

    def forward(
        self,
        char_ids: torch.Tensor,
        base_skeleton: torch.Tensor,
        ref_patches: torch.Tensor,
        target_patch: torch.Tensor,
        style_feats: torch.Tensor,
        is_missing_labels: torch.Tensor | None = None,
        contour_labels: torch.Tensor | None = None,
        metrics_labels: torch.Tensor | None = None,
        style_true_norm: torch.Tensor | None = None,
        writer_labels: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:
        B = char_ids.shape[0]
        ref_2d = ref_patches.view(B, 4, 16, 16)
        tgt_2d = target_patch.view(B, 1, 16, 16)

        ref_conv = self.ref_conv_stem(ref_2d)  # [B, 128, 8, 8]
        ref_pool = F.adaptive_avg_pool2d(ref_conv, (2, 2)).reshape(B, 128 * 4)

        tgt_conv = self.target_conv_stem(tgt_2d)  # [B, 64, 8, 8]
        tgt_pool = F.adaptive_avg_pool2d(tgt_conv, (1, 1)).reshape(B, 64)

        style_in = torch.cat([ref_pool, tgt_pool, style_feats], dim=-1)
        style_emb = self.style_projector(style_in)  # [B, style_dim]

        pred_style_norm = self.style_reg_head(style_emb)  # [B, 8]
        writer_logits = self.writer_head(style_emb)  # [B, num_writers]

        missing_in = torch.cat([tgt_pool, style_emb], dim=-1)
        missing_logits = self.missing_head(missing_in).squeeze(-1)  # [B]

        # Build 16-point token sequence for the target glyph
        pt_ids = torch.arange(self.config.num_points, device=char_ids.device).unsqueeze(0).expand(B, -1)
        c_tok = self.char_emb(char_ids).unsqueeze(1)  # [B, 1, H]
        p_tok = self.point_emb(pt_ids)  # [B, 16, H]
        b_tok = self.base_coord_proj(base_skeleton)  # [B, 16, H]
        s_tok = self.style_to_dec(torch.cat([style_emb, pred_style_norm], dim=-1)).unsqueeze(1)  # [B, 1, H]

        seq = p_tok + b_tok + c_tok + s_tok  # [B, 16, H]
        dec_out = self.glyph_transformer(seq)  # [B, 16, H]

        delta_coords = torch.tanh(self.contour_head(dec_out)) * 0.35
        contour_preds = torch.clamp(base_skeleton + delta_coords, 0.01, 0.99)

        glyph_pooled = dec_out.mean(dim=1)  # [B, H]
        metrics_in = torch.cat([glyph_pooled, style_emb, pred_style_norm], dim=-1)
        metrics_preds = self.metrics_head(metrics_in)  # [B, 5]

        out: dict[str, torch.Tensor] = {
            "missing_logits": missing_logits,
            "contour_preds": contour_preds,
            "metrics_preds": metrics_preds,
            "pred_style_norm": pred_style_norm,
            "writer_logits": writer_logits,
            "style_emb": style_emb,
        }

        if is_missing_labels is not None and contour_labels is not None and metrics_labels is not None:
            loss_missing = F.binary_cross_entropy_with_logits(missing_logits, is_missing_labels.float())

            # Mask contour & metrics loss to valid (non-missing) glyphs or supervise full style synthesis
            loss_contour = F.smooth_l1_loss(contour_preds, contour_labels, beta=0.01)

            # Edge tangent preservation loss (keeps Bézier segments smooth and faithful)
            pred_edges = torch.roll(contour_preds, -1, dims=1) - contour_preds
            true_edges = torch.roll(contour_labels, -1, dims=1) - contour_labels
            loss_edges = F.smooth_l1_loss(pred_edges, true_edges, beta=0.01)

            loss_metrics = F.smooth_l1_loss(metrics_preds, metrics_labels, beta=0.01)

            total_loss = 1.5 * loss_missing + 12.0 * loss_contour + 6.0 * loss_edges + 4.0 * loss_metrics

            if style_true_norm is not None:
                loss_style = F.smooth_l1_loss(pred_style_norm, style_true_norm, beta=0.01)
                total_loss = total_loss + 3.0 * loss_style
            if writer_labels is not None:
                loss_writer = F.cross_entropy(writer_logits, writer_labels)
                total_loss = total_loss + 0.5 * loss_writer

            out["loss"] = total_loss

        return out
