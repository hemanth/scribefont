"""Train, calibrate, and evaluate ScribeFontForGeneration on MPS / CUDA / CPU."""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import get_cosine_schedule_with_warmup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "training"))

from generate_dataset import (
    CHARSET,
    DATA_DIR,
    WRITER_ARCHETYPES,
    canonical_skeleton_points,
    main as generate_data_main,
)
from modeling_scribefont import ScribeFontConfig, ScribeFontForGeneration

ARTIFACT_DIR = ROOT / "artifacts" / "scribefont"
WRITER_TO_IDX = {w["writer_id"]: i for i, w in enumerate(WRITER_ARCHETYPES)}


def _normalize_style_true(style: list[float]) -> list[float]:
    return [
        max(0.0, min(1.0, (style[0] + 15.0) / 40.0)),
        max(0.0, min(1.0, (style[1] - 25.0) / 90.0)),
        max(0.0, min(1.0, (style[2] - 0.55) / 0.30)),
        max(0.0, min(1.0, (style[3] - 0.70) / 0.60)),
        max(0.0, min(1.0, style[4])),
        max(0.0, min(1.0, style[5] / 25.0)),
        max(0.0, min(1.0, style[6])),
        max(0.0, min(1.0, style[7])),
    ]


class ScribeFontDataset(Dataset):
    def __init__(self, jsonl_path: Path) -> None:
        self.rows = [json.loads(ln) for ln in jsonl_path.read_text().splitlines() if ln.strip()]
        self.encoded = [self._encode(r) for r in self.rows]

    def _encode(self, r: dict[str, Any]) -> dict[str, torch.Tensor]:
        ch = r["char"]
        skel = canonical_skeleton_points(ch)
        w_idx = WRITER_TO_IDX.get(r["writer_id"], 0)
        s_norm = _normalize_style_true(r["style_true"])
        return {
            "char_ids": torch.tensor(int(r["char_id"]), dtype=torch.long),
            "base_skeleton": torch.tensor(skel, dtype=torch.float32),
            "ref_patches": torch.tensor(r["ref_patches"], dtype=torch.float32),
            "target_patch": torch.tensor(r["target_patch"], dtype=torch.float32),
            "style_feats": torch.tensor(r["style_feats"], dtype=torch.float32),
            "is_missing_labels": torch.tensor(int(r["is_missing"]), dtype=torch.long),
            "contour_labels": torch.tensor(r["contour_norm"], dtype=torch.float32),
            "metrics_labels": torch.tensor(r["metrics_norm"], dtype=torch.float32),
            "style_true_norm": torch.tensor(s_norm, dtype=torch.float32),
            "writer_labels": torch.tensor(w_idx, dtype=torch.long),
        }

    def __len__(self) -> int:
        return len(self.encoded)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return self.encoded[idx]


@torch.no_grad()
def evaluate(model: ScribeFontForGeneration, loader: DataLoader, device: torch.device) -> dict[str, float]:
    model.eval()
    missing_correct, total = 0, 0
    writer_correct = 0
    contour_l1_upm: list[float] = []
    advance_err_upm: list[float] = []

    for batch in loader:
        b = {k: v.to(device) for k, v in batch.items()}
        out = model(**b)
        p_miss = torch.sigmoid(out["missing_logits"])
        preds_miss = (p_miss > 0.5).long()
        missing_correct += int((preds_miss == b["is_missing_labels"]).sum().item())
        total += b["is_missing_labels"].numel()

        w_preds = out["writer_logits"].argmax(dim=-1)
        writer_correct += int((w_preds == b["writer_labels"]).sum().item())

        # Contour error in UPM (1000 units per em)
        c_diff = (out["contour_preds"] - b["contour_labels"]).abs().mean(dim=(1, 2)) * 1000.0
        contour_l1_upm.extend(c_diff.cpu().tolist())

        adv_diff = (out["metrics_preds"][:, 0] - b["metrics_labels"][:, 0]).abs() * 1000.0
        advance_err_upm.extend(adv_diff.cpu().tolist())

    return {
        "missing_acc": round(missing_correct / max(1, total), 4),
        "writer_acc": round(writer_correct / max(1, total), 4),
        "contour_mae_upm": round(sum(contour_l1_upm) / max(1, len(contour_l1_upm)), 2),
        "advance_mae_upm": round(sum(advance_err_upm) / max(1, len(advance_err_upm)), 2),
    }


def main() -> None:
    if not (DATA_DIR / "train.jsonl").exists():
        generate_data_main()

    torch.manual_seed(20261019)
    device = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"[ScribeFont] Training on device: {device}")

    train_ds = ScribeFontDataset(DATA_DIR / "train.jsonl")
    val_ds = ScribeFontDataset(DATA_DIR / "val.jsonl")

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)

    cfg = ScribeFontConfig(
        vocab_size=len(CHARSET),
        num_writers=len(WRITER_ARCHETYPES),
        num_points=16,
        style_dim=128,
        hidden_dim=256,
        num_layers=4,
        num_heads=8,
        dropout=0.03,
    )
    model = ScribeFontForGeneration(cfg).to(device)
    param_count = sum(p.numel() for p in model.parameters())
    print(f"[ScribeFont] Parameters: {param_count:,} ({param_count / 1e6:.2f}M)")

    epochs = 28
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4, weight_decay=1e-4)
    total_steps = epochs * len(train_loader)
    scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=int(0.08 * total_steps), num_training_steps=total_steps)

    best_score = -1e9
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            b = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad()
            out = model(**b)
            loss = out["loss"]
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            running_loss += float(loss.item())

        if epoch % 4 == 0 or epoch == epochs:
            metrics = evaluate(model, val_loader, device)
            score = metrics["missing_acc"] * 100.0 + metrics["writer_acc"] * 100.0 - metrics["contour_mae_upm"]
            print(
                f"Epoch {epoch:02d}/{epochs} | loss={running_loss/len(train_loader):.4f} "
                f"| missing_acc={metrics['missing_acc']*100:.1f}% "
                f"| writer_acc={metrics['writer_acc']*100:.1f}% "
                f"| contour_mae={metrics['contour_mae_upm']:.2f} UPM "
                f"| adv_mae={metrics['advance_mae_upm']:.2f} UPM"
            )
            if score >= best_score:
                best_score = score
                model.save_pretrained(str(ARTIFACT_DIR))
                cfg.save_pretrained(str(ARTIFACT_DIR))

    shutil.copyfile(ROOT / "training" / "modeling_scribefont.py", ARTIFACT_DIR / "modeling_scribefont.py")
    elapsed = round(time.perf_counter() - t0, 2)
    final_metrics = evaluate(
        ScribeFontForGeneration.from_pretrained(str(ARTIFACT_DIR), config=cfg).to(device),
        val_loader,
        device,
    )
    summary = {
        "model": "ScribeFontForGeneration",
        "parameters": param_count,
        "device": str(device),
        "train_seconds": elapsed,
        "best_val_metrics": final_metrics,
    }
    (ARTIFACT_DIR / "training_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
