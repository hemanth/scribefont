"""Export ScribeFontForGeneration to ONNX (FP32 + Dynamic Int8 Quantized) for Browser WASM SIMD / WebGPU."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import onnx
import torch
import torch.nn as nn
from onnxruntime.quantization import QuantType, quantize_dynamic

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "training"))

from modeling_scribefont import ScribeFontConfig, ScribeFontForGeneration

ARTIFACT_DIR = ROOT / "artifacts" / "scribefont"
ONNX_DIR = ARTIFACT_DIR / "onnx"


class ScribeFontOnnxWrapper(nn.Module):
    """Pure tensor-in, tensor-tuple-out wrapper for ONNX export (WASM/WebGPU compatible ops)."""

    def __init__(self, model: ScribeFontForGeneration) -> None:
        super().__init__()
        self.model = model

    def forward(
        self,
        char_ids: torch.Tensor,
        base_skeleton: torch.Tensor,
        ref_patches: torch.Tensor,
        target_patch: torch.Tensor,
        style_feats: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        out = self.model(
            char_ids=char_ids,
            base_skeleton=base_skeleton,
            ref_patches=ref_patches,
            target_patch=target_patch,
            style_feats=style_feats,
        )
        return (
            out["missing_logits"],
            out["contour_preds"],
            out["metrics_preds"],
            out["pred_style_norm"],
            out["writer_logits"],
        )


def main() -> None:
    ONNX_DIR.mkdir(parents=True, exist_ok=True)
    cfg = ScribeFontConfig.from_pretrained(str(ARTIFACT_DIR))
    model = ScribeFontForGeneration.from_pretrained(str(ARTIFACT_DIR), config=cfg)
    model.eval()

    wrapper = ScribeFontOnnxWrapper(model)
    wrapper.eval()

    B = 2
    dummy_char = torch.tensor([0, 1], dtype=torch.long)
    dummy_skel = torch.zeros((B, 16, 2), dtype=torch.float32)
    dummy_ref = torch.zeros((B, 1024), dtype=torch.float32)
    dummy_tgt = torch.zeros((B, 256), dtype=torch.float32)
    dummy_style = torch.zeros((B, 8), dtype=torch.float32)

    fp32_path = ONNX_DIR / "model.onnx"
    int8_path = ONNX_DIR / "model_quantized.onnx"

    torch.onnx.export(
        wrapper,
        (dummy_char, dummy_skel, dummy_ref, dummy_tgt, dummy_style),
        str(fp32_path),
        input_names=["char_ids", "base_skeleton", "ref_patches", "target_patch", "style_feats"],
        output_names=["missing_logits", "contour_preds", "metrics_preds", "pred_style_norm", "writer_logits"],
        dynamic_axes={
            "char_ids": {0: "batch_size"},
            "base_skeleton": {0: "batch_size"},
            "ref_patches": {0: "batch_size"},
            "target_patch": {0: "batch_size"},
            "style_feats": {0: "batch_size"},
            "missing_logits": {0: "batch_size"},
            "contour_preds": {0: "batch_size"},
            "metrics_preds": {0: "batch_size"},
            "pred_style_norm": {0: "batch_size"},
            "writer_logits": {0: "batch_size"},
        },
        opset_version=17,
        do_constant_folding=True,
        dynamo=False,
    )

    onnx_model = onnx.load(str(fp32_path), load_external_data=True)
    onnx.save_model(onnx_model, str(fp32_path), save_as_external_data=False)
    for ext_file in ONNX_DIR.glob("*.data"):
        ext_file.unlink()

    quantize_dynamic(
        model_input=str(fp32_path),
        model_output=str(int8_path),
        weight_type=QuantType.QUInt8,
    )

    # Also copy quantized model to docs/ for local playground testing
    (ROOT / "docs").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(int8_path, ROOT / "docs" / "model_quantized.onnx")

    fp32_mb = round(fp32_path.stat().st_size / (1024 * 1024), 2)
    int8_mb = round(int8_path.stat().st_size / (1024 * 1024), 2)
    summary = {
        "onnx_fp32_path": str(fp32_path),
        "onnx_fp32_size_mb": fp32_mb,
        "onnx_int8_path": str(int8_path),
        "onnx_int8_size_mb": int8_mb,
        "compression_ratio": round(fp32_mb / max(0.05, int8_mb), 2),
    }
    (ONNX_DIR / "export_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
