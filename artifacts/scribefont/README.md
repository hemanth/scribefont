---
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

# `scribefont` — Empirical & Statistical Evaluation Report (`SCIENCE_REPORT.md`)

> **Reproducibility**: All numbers in this report are produced deterministically by `python bench/run_bench.py` (`seed=20261019`, `B=1,000` bootstrap resamples) and stored in [`bench/results.json`](./results.json).

---

## 1. Architectural Tiering & Deployment Matrix

Following the 3-tier scientific module playbook, `scribefont` separates **2D Convolutional + Transformer neural style-conditioned glyph generation** from **deterministic zero-dependency Bézier vectorization & binary TrueType (`.ttf`) compilation**:

| Architectural Tier | Runtime / Artifact | Disk Footprint | Parameter Count | Primary Use Case |
| :--- | :--- | :---: | :---: | :--- |
| **Tier 1A: Neural Style-Conditioned (FP32)** | [`gnumanth/scribefont`](https://huggingface.co/gnumanth/scribefont) (`model.safetensors`) | `11.4 MB` | `2.94M` (`Conv2d` + `4-Layer Transformer`) | Few-shot unseen glyph synthesis from noisy camera scans, writer style extraction |
| **Tier 1B: Neural Quantized (Int8 ONNX)** | [`onnx/model_quantized.onnx`](https://huggingface.co/gnumanth/scribefont/tree/main/onnx) (`onnxruntime-web` WASM SIMD / CPU) | `3.15 MB` (`3.62x` smaller) | `2.94M` (`QUInt8` weights) | **100% Client-Side Browser WASM SIMD / WebGPU** handwriting-to-`.ttf` studio |
| **Tier 2: Zero-Dep Fast Engine** | `npm i scribefont` / `pip install scribefont` | `0.0 MB` (`~18 KB` code) | `0` (Deterministic Bézier + `.ttf` packer) | Ultra-low-latency (`0.0747 ms/glyph`) parametric glyph synthesis & binary `.ttf` compilation |

---

## 2. Suite A: Wild Camera-Scan Few-Shot Unseen-Glyph Generalization ($N=60$)

Evaluates synthesizing unseen target characters (`30` valid unseen glyphs + `30` blank/smudged cells) from only `4` noisy `16x16` reference handwriting crops (`'A'`, `'g'`, `'m'`, `'R'`) when explicit biometric headers are stripped/corrupted by camera noise:

| Metric ($N=60$, $B=1,000$ Bootstrap 95% CI) | Tier 1A: PyTorch FP32 Neural | Tier 1B: ONNX Int8 Quantized (WASM/CPU) | Tier 2: Zero-Dep Geometric Engine |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy (95% Bootstrap CI)** | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` | 80.0% `[70.0, 90.0]` |
| **Unseen-Glyph Style Fidelity (`MAE < 12 UPM`)** | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` | 60.0% `[40.0, 76.67]` |
| **Bézier Contour Coordinate MAE (`UPM`, lower is better)** | **2.38 UPM** | **2.39 UPM** | 11.13 UPM |
| **Advance-Width Prediction MAE (`UPM`)** | **13.93 UPM** | **14.02 UPM** | 35.5 UPM |
| **12-Writer Calligrapher Identification Accuracy** | **100.0%** | **100.0%** | 16.67% |
| **Blank/Smudge Cell Abstention (`p_missing > 0.5`)** | **100.0%** | **100.0%** | **100.0%** |
| **Abstention `p_missing` AUROC / 10-Bin ECE** | **1.0** / `0.00276` | **1.0** / `0.00282` | **1.0** / `0.0006` |
| **Latency `p50` / `p95` / `p99` (ms/glyph)** | `6.1797` / `8.3667` / `9.2688 ms` | `1.2708` / `1.5253` / `1.5695 ms` | **0.0539** / `0.0632` / `0.0716 ms` |

---

## 3. Suite B: Structured 62-Glyph Full-Alphabet Synthesis & OpenType `.ttf` Suite ($N=62$)

Evaluates full-alphabet (`A-Z`, `a-z`, `0-9`) glyph contour synthesis, metric invariants (`advance_width >= bbox_width + lsb`), and binary TrueType (`.ttf`) compilation (`0xB1B0AFBA` master checksum verification):

| Metric ($N=62$ alphanumeric glyphs) | Tier 1A: PyTorch FP32 Neural | Tier 1B: ONNX Int8 Quantized | Tier 2: Zero-Dep Fast Engine |
| :--- | :---: | :---: | :---: |
| **Glyph Fidelity Accuracy (95% Bootstrap CI)** | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` |
| **Bézier Contour MAE (`UPM`, out of `1000 UPM`)** | `0.98 UPM` | `0.98 UPM` | **0.0 UPM** |
| **OpenType Metric Invariant (`adv >= w + lsb`)** | **100.0%** | **100.0%** | **100.0%** |
| **Compiled Binary `.ttf` Checksum & SFNT Validity** | **100.0%** (`7292 B`) | **100.0%** (`7292 B`) | **100.0%** (`7292 B`) |
| **Per-Glyph Latency `p50` / `p95` (ms)** | `6.035` / `9.1311 ms` | `1.3858` / `1.9749 ms` | **0.0747** / `0.083 ms` |

---

## 4. Suite C: Adversarial Ink-Smudge & Blank-Cell Abstention Stress Suite ($N=12$)

| Adversarial Stress Metric ($N=12$) | Tier 1A: PyTorch FP32 Neural | Tier 1B: ONNX Int8 Quantized | Tier 2: Zero-Dep Fast Engine |
| :--- | :---: | :---: | :---: |
| **Adversarial Glyph & Abstention Accuracy (95% CI)** | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` | **100.0%** `[100.0, 100.0]` |
| **Calibrated `p_missing` AUROC** | **1.0** | **1.0** | **1.0** |
| **Abstention 10-Bin ECE / Brier Score** | `0.00077` / `0.0` | `0.00077` / `0.0` | `0.0006` / `0.0` |

