"""Generate multi-writer Handwriting-to-Font training, validation, and benchmark datasets."""
from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

from glyph_skeletons import (
    CHARSET,
    CHAR_TO_ID,
    GLYPH_STROKES,
    canonical_skeleton_points,
    split_16pts_into_strokes,
)

# 12 canonical calligrapher writer archetypes with 8 biometric style dimensions:
# [slant_deg, stroke_width_upm, x_height_ratio, width_scale, roundness, baseline_jitter, contrast, serif_flare]
WRITER_ARCHETYPES: list[dict[str, Any]] = [
    {
        "writer_id": "w01_architect",
        "name": "Architect Blueprint",
        "style": [4.0, 58.0, 0.70, 1.04, 0.25, 2.0, 0.12, 0.35],
    },
    {
        "writer_id": "w02_copperplate",
        "name": "Slanted Copperplate",
        "style": [18.5, 42.0, 0.63, 0.92, 0.85, 3.5, 0.58, 0.65],
    },
    {
        "writer_id": "w03_studio_sans",
        "name": "Rounded Studio Sans",
        "style": [0.0, 72.0, 0.75, 1.08, 0.92, 1.0, 0.06, 0.05],
    },
    {
        "writer_id": "w04_monoline_eng",
        "name": "Monoline Engineer",
        "style": [2.5, 52.0, 0.69, 0.96, 0.40, 1.5, 0.08, 0.15],
    },
    {
        "writer_id": "w05_felt_marker",
        "name": "Heavy Felt Marker",
        "style": [6.0, 102.0, 0.76, 1.16, 0.78, 5.0, 0.18, 0.08],
    },
    {
        "writer_id": "w06_field_notes",
        "name": "Jittery Field Notes",
        "style": [11.0, 48.0, 0.66, 0.89, 0.55, 16.0, 0.28, 0.22],
    },
    {
        "writer_id": "w07_condensed_ed",
        "name": "Condensed Editorial",
        "style": [-3.5, 46.0, 0.64, 0.81, 0.32, 2.5, 0.44, 0.52],
    },
    {
        "writer_id": "w08_draftsman_wide",
        "name": "Wide Draftsman",
        "style": [1.5, 64.0, 0.73, 1.22, 0.48, 1.8, 0.14, 0.28],
    },
    {
        "writer_id": "w09_italic_nib",
        "name": "Italic Nib Script",
        "style": [15.0, 54.0, 0.67, 0.95, 0.74, 4.0, 0.52, 0.48],
    },
    {
        "writer_id": "w10_editorial_serif",
        "name": "High-Contrast Serif",
        "style": [0.5, 56.0, 0.68, 1.02, 0.60, 1.2, 0.62, 0.75],
    },
    {
        "writer_id": "w11_lab_notebook",
        "name": "Compact Lab Notebook",
        "style": [7.5, 50.0, 0.71, 0.91, 0.64, 8.5, 0.20, 0.18],
    },
    {
        "writer_id": "w12_bouncy_casual",
        "name": "Bouncy Casual",
        "style": [-6.0, 68.0, 0.74, 1.09, 0.88, 14.0, 0.15, 0.10],
    },
]


def apply_writer_style_to_glyph(
    ch: str,
    style: list[float],
    upm: int = 1000,
) -> dict[str, Any]:
    """Synthesize ground-truth glyph contour, metrics, and normalized deltas for a writer."""
    slant_deg, stroke_w, x_ratio, w_scale, roundness, jitter, contrast, flare = style
    slant_tan = math.tan(math.radians(slant_deg))

    base_pts = canonical_skeleton_points(ch)
    is_lower = "a" <= ch <= "z" and ch not in "bdfhklt"
    y_scale = (x_ratio / 0.70) if is_lower else 1.0

    char_hash = ((CHAR_TO_ID.get(ch, 0) * 131 + 17) % 100) / 100.0 - 0.5
    y_jitter_norm = (jitter * char_hash) / upm

    contour_norm: list[list[float]] = []
    contour_upm: list[list[int]] = []

    for i, (bx, by) in enumerate(base_pts):
        dy = (by - 0.22) * y_scale + 0.22 + y_jitter_norm
        dx = 0.5 + (bx - 0.5) * w_scale + (dy - 0.5) * slant_tan * 0.35
        rad_mod = (roundness - 0.5) * 0.025 * math.cos(i * math.pi / 4.0)
        flare_mod = flare * 0.02 if i in (0, 15) else 0.0
        nx = max(0.02, min(0.98, dx + rad_mod + flare_mod))
        ny = max(0.01, min(0.99, dy - rad_mod * 0.4))
        contour_norm.append([round(nx, 5), round(ny, 5)])

        ux = int(round(nx * upm * 0.68))
        uy = int(round((ny - 0.22) * upm))
        contour_upm.append([ux, uy])

    xs = [p[0] for p in contour_upm]
    ys = [p[1] for p in contour_upm]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    lsb = max(20, int(round(xmin * 0.85)))
    bbox_w = max(120, xmax - xmin + int(stroke_w * 0.8))
    advance_width = int(round(lsb + bbox_w + max(28.0, stroke_w * 0.55)))
    kern_av = int(round(-45.0 * w_scale - abs(slant_deg) * 1.2 - flare * 12.0))

    return {
        "char": ch,
        "char_id": CHAR_TO_ID.get(ch, 0),
        "contour_norm": contour_norm,
        "contour_upm": contour_upm,
        "bbox": [xmin, ymin, xmax, ymax],
        "lsb": lsb,
        "advance_width": advance_width,
        "stroke_width": round(stroke_w, 2),
        "slant_deg": round(slant_deg, 2),
        "x_height_ratio": round(x_ratio, 4),
        "kern_av": kern_av,
    }


def render_glyph_patch_16x16(
    contour_norm: list[list[float]],
    stroke_w: float,
    contrast: float,
    noise_std: float = 0.0,
    rng: random.Random | None = None,
    blank: bool = False,
    ch: str = "A",
) -> list[float]:
    """Rasterize a 16x16 signed-distance / ink intensity patch (256 floats in [0, 1]) over open strokes."""
    r = rng or random.Random(42)
    if blank:
        return [round(max(0.0, min(0.22, r.gauss(0.03, 0.04))), 4) for _ in range(256)]

    strokes = split_16pts_into_strokes(ch, contour_norm)
    radius = max(0.045, min(0.14, stroke_w / 950.0))
    grid: list[float] = []
    for gy in range(16):
        py = (15 - gy + 0.5) / 16.0
        for gx in range(16):
            px = (gx + 0.5) / 16.0
            min_d = 9.0
            best_seg = 0
            for s_idx, stroke in enumerate(strokes):
                for i in range(len(stroke) - 1):
                    ax, ay = stroke[i]
                    bx, by = stroke[i + 1]
                    vx, vy = bx - ax, by - ay
                    wx, wy = px - ax, py - ay
                    c1 = vx * wx + vy * wy
                    c2 = vx * vx + vy * vy
                    t = 0.0 if c2 <= 1e-9 else max(0.0, min(1.0, c1 / c2))
                    proj_x = ax + t * vx
                    proj_y = ay + t * vy
                    d = math.hypot(px - proj_x, py - proj_y)
                    if d < min_d:
                        min_d = d
                        best_seg = i + s_idx
            local_r = radius * (1.0 - 0.35 * contrast * (best_seg % 2))
            ink = 1.0 / (1.0 + math.exp((min_d - local_r) / 0.025))
            if noise_std > 0.0:
                ink += r.gauss(0.0, noise_std)
            grid.append(round(max(0.0, min(1.0, ink)), 4))
    return grid


def make_writer_reference_features(
    style: list[float],
    rng: random.Random,
    noise_level: float = 0.02,
    corrupt_lexical_header: bool = False,
) -> tuple[list[float], list[float]]:
    """Produce:
    1) `ref_patches_flat`: 4 canonical reference glyphs ('A', 'g', 'm', 'R') rasterized as 4 x 16x16 = 1024 floats
    2) `style_summary_feats`: 8 biometric summary features (corrupted if camera/wild noise is high)
    """
    ref_chars = ("A", "g", "m", "R")
    patches: list[float] = []
    for rc in ref_chars:
        g = apply_writer_style_to_glyph(rc, style)
        patch = render_glyph_patch_16x16(
            g["contour_norm"],
            style[1],
            style[6],
            noise_std=noise_level,
            rng=rng,
        )
        patches.extend(patch)

    # Normalize 8 style features to [0, 1]
    norm_style = [
        (style[0] + 15.0) / 40.0,        # slant_deg in [-15, 25]
        (style[1] - 25.0) / 90.0,        # stroke_width in [25, 115]
        (style[2] - 0.55) / 0.30,        # x_height_ratio in [0.55, 0.85]
        (style[3] - 0.70) / 0.60,        # width_scale in [0.70, 1.30]
        style[4],                        # roundness in [0, 1]
        style[5] / 25.0,                 # baseline_jitter in [0, 25]
        style[6],                        # contrast in [0, 1]
        style[7],                        # serif_flare in [0, 1]
    ]
    if corrupt_lexical_header:
        # In wild camera scans without pre-extracted biometric headers, the explicit metadata header is zeroed/noisy,
        # forcing the model to infer writer style purely from the 2D visual reference patches!
        summary = [round(0.5 + rng.gauss(0.0, 0.05), 4) for _ in range(8)]
    else:
        summary = [round(max(0.0, min(1.0, v)), 4) for v in norm_style]
    return patches, summary


def perturb_style(base_style: list[float], rng: random.Random, scale: float = 0.08) -> list[float]:
    return [
        max(-12.0, min(22.0, base_style[0] + rng.gauss(0.0, 1.8 * scale * 10))),
        max(30.0, min(110.0, base_style[1] + rng.gauss(0.0, 4.5 * scale * 10))),
        max(0.58, min(0.80, base_style[2] + rng.gauss(0.0, 0.015 * scale * 10))),
        max(0.75, min(1.26, base_style[3] + rng.gauss(0.0, 0.025 * scale * 10))),
        max(0.10, min(0.96, base_style[4] + rng.gauss(0.0, 0.04 * scale * 10))),
        max(0.5, min(22.0, base_style[5] + rng.gauss(0.0, 1.2 * scale * 10))),
        max(0.04, min(0.75, base_style[6] + rng.gauss(0.0, 0.03 * scale * 10))),
        max(0.02, min(0.85, base_style[7] + rng.gauss(0.0, 0.03 * scale * 10))),
    ]


def build_training_row(
    writer_id: str,
    style: list[float],
    ch: str,
    rng: random.Random,
    is_missing: int = 0,
    wild_camera_scan: bool = False,
) -> dict[str, Any]:
    g = apply_writer_style_to_glyph(ch, style)
    ref_patches, style_feats = make_writer_reference_features(
        style,
        rng,
        noise_level=0.06 if wild_camera_scan else 0.015,
        corrupt_lexical_header=wild_camera_scan,
    )
    target_patch = render_glyph_patch_16x16(
        g["contour_norm"],
        style[1],
        style[6],
        noise_std=0.05 if wild_camera_scan else 0.01,
        rng=rng,
        blank=(is_missing == 1),
    )

    metrics_norm = [
        round(g["advance_width"] / 1000.0, 5),
        round(g["lsb"] / 300.0, 5),
        round((g["slant_deg"] + 15.0) / 40.0, 5),
        round(g["stroke_width"] / 120.0, 5),
        round((g["kern_av"] + 120.0) / 120.0, 5),
    ]

    return {
        "writer_id": writer_id,
        "char": ch,
        "char_id": g["char_id"],
        "is_missing": is_missing,
        "wild_camera_scan": wild_camera_scan,
        "style_true": [round(x, 4) for x in style],
        "style_feats": style_feats,
        "ref_patches": ref_patches,
        "target_patch": target_patch,
        "contour_norm": g["contour_norm"],
        "metrics_norm": metrics_norm,
        "ground_truth_upm": {
            "advance_width": g["advance_width"],
            "lsb": g["lsb"],
            "bbox": g["bbox"],
            "stroke_width": g["stroke_width"],
            "slant_deg": g["slant_deg"],
            "kern_av": g["kern_av"],
        },
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261019)

    train_rows: list[dict[str, Any]] = []
    val_rows: list[dict[str, Any]] = []

    # Generate 1,100 training rows and 240 validation rows across all 12 writer archetypes & 62 glyphs
    for idx in range(1100):
        arch = WRITER_ARCHETYPES[idx % len(WRITER_ARCHETYPES)]
        style = perturb_style(arch["style"], rng, scale=0.06)
        ch = CHARSET[idx % len(CHARSET)]
        is_missing = 1 if (idx % 9 == 0) else 0
        wild_scan = (idx % 2 == 0)
        train_rows.append(
            build_training_row(arch["writer_id"], style, ch, rng, is_missing=is_missing, wild_camera_scan=wild_scan)
        )

    for idx in range(240):
        arch = WRITER_ARCHETYPES[idx % len(WRITER_ARCHETYPES)]
        style = perturb_style(arch["style"], rng, scale=0.04)
        ch = CHARSET[(idx * 7) % len(CHARSET)]
        is_missing = 1 if (idx % 6 == 0) else 0
        wild_scan = (idx % 2 == 1)
        val_rows.append(
            build_training_row(arch["writer_id"], style, ch, rng, is_missing=is_missing, wild_camera_scan=wild_scan)
        )

    # Suite A: Canonical Wild-Scan Few-Shot Unseen-Glyph Benchmark (N=60: 30 valid unseen glyphs + 30 blank/corrupt abstentions)
    suite_a_rows: list[dict[str, Any]] = []
    for idx in range(60):
        arch = WRITER_ARCHETYPES[idx % len(WRITER_ARCHETYPES)]
        style = arch["style"]
        ch = CHARSET[(idx * 5 + 3) % len(CHARSET)]
        is_missing = 1 if idx >= 30 else 0
        row = build_training_row(
            arch["writer_id"],
            style,
            ch,
            rng,
            is_missing=is_missing,
            wild_camera_scan=True,
        )
        row["archetype_id"] = idx % len(WRITER_ARCHETYPES)
        suite_a_rows.append(row)

    # Suite B: Structured 62-Glyph Full-Alphabet Synthesis & OpenType Invariant Suite (N=62)
    suite_b_rows: list[dict[str, Any]] = []
    for idx, ch in enumerate(CHARSET):
        arch = WRITER_ARCHETYPES[idx % len(WRITER_ARCHETYPES)]
        style = arch["style"]
        row = build_training_row(
            arch["writer_id"],
            style,
            ch,
            rng,
            is_missing=0,
            wild_camera_scan=False,
        )
        row["archetype_id"] = idx % len(WRITER_ARCHETYPES)
        suite_b_rows.append(row)

    # Suite C: Adversarial Ink-Blot, Missing-Glyph Abstention & Decoy Stroke Suite (N=12)
    suite_c_rows: list[dict[str, Any]] = []
    for idx in range(12):
        arch = WRITER_ARCHETYPES[idx % len(WRITER_ARCHETYPES)]
        style = arch["style"]
        ch = CHARSET[(idx * 11) % len(CHARSET)]
        is_missing = 1 if (idx % 2 == 1) else 0
        row = build_training_row(
            arch["writer_id"],
            style,
            ch,
            rng,
            is_missing=is_missing,
            wild_camera_scan=False,
        )
        row["archetype_id"] = idx % len(WRITER_ARCHETYPES)
        row["adversarial_type"] = "ink_smudge_blank_cell" if is_missing else "stray_border_artifact"
        suite_c_rows.append(row)

    (DATA_DIR / "train.jsonl").write_text("\n".join(json.dumps(r) for r in train_rows) + "\n")
    (DATA_DIR / "val.jsonl").write_text("\n".join(json.dumps(r) for r in val_rows) + "\n")
    (DATA_DIR / "suite_a_wild.json").write_text(json.dumps(suite_a_rows, indent=2))
    (DATA_DIR / "suite_b_structured.json").write_text(json.dumps(suite_b_rows, indent=2))
    (DATA_DIR / "suite_c_adversarial.json").write_text(json.dumps(suite_c_rows, indent=2))

    print(
        json.dumps(
            {
                "train_count": len(train_rows),
                "val_count": len(val_rows),
                "suite_a_wild_count": len(suite_a_rows),
                "suite_b_structured_count": len(suite_b_rows),
                "suite_c_adversarial_count": len(suite_c_rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
