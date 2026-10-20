"""Publish ScribeFont model, quantized ONNX weights, dataset, and interactive Space to Hugging Face Hub."""
from __future__ import annotations

import shutil
from pathlib import Path
from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = ROOT / "artifacts" / "scribefont"
DATA_DIR = ROOT / "data"
SPACE_DIR = ROOT / "space"

MODEL_REPO = "gnumanth/scribefont"
DATASET_REPO = "gnumanth/scribefont-dataset"
SPACE_REPO = "gnumanth/scribefont"


def main() -> None:
    api = HfApi()

    # 1. Create and upload Model Repo (FP32 safetensors + Int8 ONNX)
    api.create_repo(repo_id=MODEL_REPO, repo_type="model", exist_ok=True)
    science_md = (ROOT / "bench" / "SCIENCE_REPORT.md").read_text()
    model_card = f"""---
license: mit
library_name: transformers
tags:
  - handwriting
  - font-generation
  - truetype
  - opentype
  - bezier
  - onnx
  - wasm
datasets:
  - gnumanth/scribefont-dataset
---

# ScribeFont (`gnumanth/scribefont`)

Compact `2.94M`-parameter 2D Convolutional + 4-Layer Cross-Attention Transformer for **single-pass Handwriting-to-Font synthesis**, 16-point quadratic Bézier contour generation, optical kerning prediction, and calibrated `p_missing` abstention.

Ships with:
- **Tier 1A (PyTorch FP32)**: `model.safetensors` (`11.40 MB`)
- **Tier 1B (Browser ONNX Int8 Quantized)**: `onnx/model_quantized.onnx` (`3.15 MB`, `3.62x` smaller for `onnxruntime-web` WASM SIMD)
- **Tier 2 (Zero-Dep JS/Python Engine)**: `npm install scribefont` / `pip install scribefont` (`0.0 MB` weights, `0.031 ms/glyph`)

- **Interactive Studio**: https://hemanth.github.io/scribefont/
- **GitHub Repository**: https://github.com/hemanth/scribefont

{science_md}
"""
    (ARTIFACT_DIR / "README.md").write_text(model_card)
    api.upload_folder(
        folder_path=str(ARTIFACT_DIR),
        repo_id=MODEL_REPO,
        repo_type="model",
        commit_message="Upload ScribeFont FP32 safetensors + Int8 quantized ONNX + empirical report",
    )
    print(f"Uploaded model: https://huggingface.co/{MODEL_REPO}")

    # 2. Create and upload Dataset Repo
    api.create_repo(repo_id=DATASET_REPO, repo_type="dataset", exist_ok=True)
    ds_card = """---
license: mit
task_categories:
  - image-to-text
  - other
tags:
  - handwriting
  - typography
  - font
  - bezier
---

# ScribeFont Multi-Writer Handwriting-to-Font Dataset (`gnumanth/scribefont-dataset`)

Contains `1,100` training examples, `240` validation examples, and `3` evaluation benchmark suites (`suite_a_wild.json`, `suite_b_structured.json`, `suite_c_adversarial.json`) across `12` calligrapher archetypes (`62` alphanumeric characters, 16-point normalized quadratic Bézier contours, `16x16` SDF ink patches, and OpenType `1000 UPM` metrics).
"""
    (DATA_DIR / "README.md").write_text(ds_card)
    api.upload_folder(
        folder_path=str(DATA_DIR),
        repo_id=DATASET_REPO,
        repo_type="dataset",
        commit_message="Upload ScribeFont training, validation, and 3-suite evaluation datasets",
    )
    print(f"Uploaded dataset: https://huggingface.co/datasets/{DATASET_REPO}")

    # 3. Create and upload Static Hugging Face Space
    SPACE_DIR.mkdir(parents=True, exist_ok=True)
    api.create_repo(repo_id=SPACE_REPO, repo_type="space", space_sdk="static", exist_ok=True)
    for fname in ("index.html", "bench.html", "flow-diagram.svg", "model_quantized.onnx"):
        src = ROOT / "docs" / fname
        if src.exists():
            shutil.copyfile(src, SPACE_DIR / fname)
    space_readme = """---
title: ScribeFont Studio
emoji: ✒️
colorFrom: indigo
colorTo: gray
sdk: static
pinned: false
license: mit
---

# ScribeFont — Interactive Handwriting-to-Font Studio (WASM ONNX Int8 + Zero-Dep JS)
"""
    (SPACE_DIR / "README.md").write_text(space_readme)
    api.upload_folder(
        folder_path=str(SPACE_DIR),
        repo_id=SPACE_REPO,
        repo_type="space",
        commit_message="Deploy ScribeFont interactive browser studio (WASM ONNX Int8 + Zero-Dep .ttf compiler)",
    )
    print(f"Uploaded Space: https://huggingface.co/spaces/{SPACE_REPO}")


if __name__ == "__main__":
    main()
