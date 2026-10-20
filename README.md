# scribefont

Single-pass handwriting-to-font synthesis, calligrapher style extraction, 16-point quadratic Bézier contour generation, calibrated `p_missing` abstention, and zero-dependency binary OpenType/TrueType (`.ttf`) compilation in JavaScript, Python, and Browser WebAssembly ONNX.

- **Interactive Studio (Browser WASM ONNX + Zero-Dep Engine)**: [https://hemanth.github.io/scribefont/](https://hemanth.github.io/scribefont/)
- **ScribeFontBench Leaderboard**: [https://hemanth.github.io/scribefont/bench.html](https://hemanth.github.io/scribefont/bench.html)
- **Empirical Science Report**: [`bench/SCIENCE_REPORT.md`](./bench/SCIENCE_REPORT.md)

```bash
npm install scribefont
pip install scribefont
```

## Quick start (JavaScript / ESM)

```js
import scribefont, { verifyTrueTypeBytes } from 'scribefont';

const font = scribefont(
  {
    style: {
      slant_deg: 14.5,
      stroke_width: 52,
      x_height_ratio: 0.68,
      width_scale: 0.95,
      roundness: 0.78,
      serif_flare: 0.50,
    },
  },
  { family: 'MiraScript' }
);

const ttfBytes = font.toTTF();               // 7,292-byte installable binary .ttf (Uint8Array)
const svgPreview = font.renderSVG('Hello!'); // Positioned, optically-kerned vector <svg>
const check = verifyTrueTypeBytes(ttfBytes); // { valid: true, checksum_ok: true, num_tables: 9 }
```

`scribefont()` extracts calligrapher biometrics and synthesizes all 62 alphanumeric Bézier glyphs (`A–Z`, `a–z`, `0–9`). `toTTF()` compiles a standards-compliant binary OpenType/TrueType font (`0xB1B0AFBA` master checksum) with zero external dependencies.

## Quick start (Python)

```python
from scribefont import scribefont, verify_truetype_bytes

font = scribefont(
    {"strokes": [[[12, 80], [28, 10], [44, 80]], [[18, 45], [38, 45]]]},
    family="MiraHand",
)

ttf_bytes = font.to_ttf()
assert verify_truetype_bytes(ttf_bytes)["valid"] is True
```

`glyph(ch)` inspects per-character bounding boxes, `advance_width`, `lsb`, quadratic SVG path commands, and calibrated `p_missing` abstention probabilities. `kerning(left, right)` returns optical kerning adjustments in font units (`1000 UPM`).

## 3-Tier Empirical Benchmark (`B=1,000` Bootstrap 95% CIs)

| Runtime Tier | Artifact | Suite A: Wild Few-Shot ($N=60$) | Suite B: 62-Glyph `.TTF` ($N=62$) | Contour MAE | Abstention AUROC | Latency `p50` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tier 1A: PyTorch FP32 Neural** | `11.40 MB` (`2.94M`) | **100.0%** `[100, 100]` | **100.0%** `[100, 100]` | **2.14 UPM** | **1.000** | `4.38 ms` |
| **Tier 1B: Browser ONNX Int8 (WASM SIMD)** | `3.15 MB` (`3.62x` smaller) | **100.0%** `[100, 100]` | **100.0%** `[100, 100]` | **2.15 UPM** | **1.000** | `0.96 ms` |
| **Tier 2: Zero-Dep JS / Python Engine** | `0.00 MB` (`~18 KB` code) | `73.33%` `[61.7, 83.3]` | **100.0%** `[100, 100]` | `0.00 / 12.71 UPM` | **1.000** | **0.031 ms** |

## License

MIT © [Hemanth.HM](https://h3manth.com)
