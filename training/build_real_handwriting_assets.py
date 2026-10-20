"""Extract real multi-contour handwritten vector outlines & generate real handwriting sample sheet PNGs."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "docs" / "samples"
CHARSET_FULL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?.,-"


def rdp_open(pts: list[list[float]], eps: float) -> list[list[float]]:
    if len(pts) <= 2:
        return pts
    ax, ay = pts[0]
    bx, by = pts[-1]
    vx, vy = bx - ax, by - ay
    c2 = vx * vx + vy * vy
    max_d = -1.0
    idx = 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        if c2 <= 1e-9:
            d = math.hypot(px - ax, py - ay)
        else:
            t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / c2))
            d = math.hypot(px - (ax + t * vx), py - (ay + t * vy))
        if d > max_d:
            max_d = d
            idx = i
    if max_d > eps:
        left = rdp_open(pts[: idx + 1], eps)
        right = rdp_open(pts[idx:], eps)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def simplify_closed_loop(pts: list[list[float]], eps: float = 5.5) -> list[list[int]]:
    if len(pts) < 6:
        return [[int(round(p[0])), int(round(p[1]))] for p in pts]
    mid = len(pts) // 2
    p1 = rdp_open(pts[: mid + 1], eps)
    p2 = rdp_open(pts[mid:] + [pts[0]], eps)
    res = p1[:-1] + p2[:-1]
    if len(res) < 4:
        res = pts[:: max(1, len(pts) // 6)]
    return [[int(round(p[0])), int(round(p[1]))] for p in res]


def trace_bitmap_to_contours(
    mask: list[list[int]],
    baseline_row: float,
    x_offset: float,
    scale_upm: float,
    eps: float = 5.5,
) -> list[list[list[int]]]:
    """Trace all outer boundaries and inner holes of a binary glyph bitmap into UPM contours."""
    H = len(mask)
    W = len(mask[0]) if H else 0
    adj: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for r in range(H):
        row = mask[r]
        for c in range(W):
            if not row[c]:
                continue
            if r == 0 or not mask[r - 1][c]:
                adj.setdefault((c, r), []).append((c + 1, r))
            if c == W - 1 or not row[c + 1]:
                adj.setdefault((c + 1, r), []).append((c + 1, r + 1))
            if r == H - 1 or not mask[r + 1][c]:
                adj.setdefault((c + 1, r + 1), []).append((c, r + 1))
            if c == 0 or not row[c - 1]:
                adj.setdefault((c, r + 1), []).append((c, r))

    contours: list[list[list[int]]] = []
    while adj:
        start = next(iter(adj))
        curr = start
        loop: list[tuple[int, int]] = []
        while True:
            loop.append(curr)
            nxts = adj.get(curr)
            if not nxts:
                break
            nxt = nxts.pop()
            if not nxts:
                del adj[curr]
            curr = nxt
            if curr == start:
                break
        if len(loop) >= 10:
            pts = [[(p[0] - x_offset) * scale_upm, (baseline_row - p[1]) * scale_upm] for p in loop]
            for _ in range(2):
                n = len(pts)
                pts = [
                    [
                        0.25 * pts[(i - 1) % n][0] + 0.5 * pts[i][0] + 0.25 * pts[(i + 1) % n][0],
                        0.25 * pts[(i - 1) % n][1] + 0.5 * pts[i][1] + 0.25 * pts[(i + 1) % n][1],
                    ]
                    for i in range(n)
                ]
            simp = simplify_closed_loop(pts, eps=eps)
            if len(simp) >= 4:
                contours.append(simp)
    return contours


def contours_to_svg_d(contours: list[list[list[int]]]) -> str:
    """Convert multi-contour UPM loops (outer + inner holes) into a smooth quadratic Bézier SVG path."""
    parts: list[str] = []
    for loop in contours:
        n = len(loop)
        if n < 3:
            continue
        mid0_x = int(round(0.5 * (loop[-1][0] + loop[0][0])))
        mid0_y = int(round(0.5 * (loop[-1][1] + loop[0][1])))
        parts.append(f"M {mid0_x} {mid0_y}")
        for i in range(n):
            curr = loop[i]
            nxt = loop[(i + 1) % n]
            mx = int(round(0.5 * (curr[0] + nxt[0])))
            my = int(round(0.5 * (curr[1] + nxt[1])))
            parts.append(f"Q {curr[0]} {curr[1]} {mx} {my}")
        parts.append("Z")
    return " ".join(parts)


def extract_font_glyph_bank(font_path: str, font_size: int = 110) -> dict[str, dict[str, Any]]:
    """Render and vector-trace all 67 characters from a real handwriting font into compact UPM multi-contours."""
    f = ImageFont.truetype(font_path, font_size)
    ascent, descent = f.getmetrics()
    scale_upm = 740.0 / max(1.0, float(ascent))
    bank: dict[str, dict[str, Any]] = {}

    for ch in CHARSET_FULL:
        W, H = 180, 200
        im = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(im)
        origin_x, origin_y = 24, 24
        dr.text((origin_x, origin_y), ch, fill=255, font=f)
        baseline_y = origin_y + ascent

        arr = np.array(im)
        ys, xs = np.where(arr > 110)
        if len(xs) == 0:
            continue
        x_min_px = max(0, int(xs.min()) - 2)
        mask = (arr > 110).astype(int).tolist()
        contours = trace_bitmap_to_contours(
            mask,
            baseline_row=float(baseline_y),
            x_offset=float(x_min_px) - 5.0,
            scale_upm=scale_upm,
            eps=6.5,
        )
        all_pts = [pt for c in contours for pt in c]
        if not all_pts:
            continue
        ux = [p[0] for p in all_pts]
        uy = [p[1] for p in all_pts]
        xmin, xmax = min(ux), max(ux)
        ymin, ymax = min(uy), max(uy)
        lsb = max(18, xmin)
        adv = max(240, xmax + 48)
        bank[ch] = {
            "contours": contours,
            "bbox": [xmin, ymin, xmax, ymax],
            "lsb": lsb,
            "advance_width": adv,
        }
    return bank


def render_handwriting_sample_sheet(
    font_path: str,
    out_path: Path,
    paper_rgb: tuple[int, int, int] = (252, 250, 244),
    ink_rgb: tuple[int, int, int] = (24, 26, 32),
) -> str:
    """Render a realistic handwritten sample sheet image containing all 62 characters + pangram."""
    lines = [
        "ABCDEFGHIJKLM",
        "NOPQRSTUVWXYZ",
        "abcdefghijklm",
        "nopqrstuvwxyz",
        "0123456789!?.",
    ]
    W, H = 920, 460
    im = Image.new("RGB", (W, H), paper_rgb)
    # Add subtle realistic lighting vignette & paper grain
    arr = np.array(im, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    vignette = 1.0 - 0.06 * (((xx - W * 0.5) / (W * 0.6)) ** 2 + ((yy - H * 0.5) / (H * 0.6)) ** 2)
    rng = np.random.default_rng(20261020)
    grain = rng.normal(0.0, 2.2, size=(H, W, 1))
    arr = np.clip(arr * vignette[:, :, None] + grain, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)

    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(font_path, 46)
    for row_idx, line in enumerate(lines):
        y = 18 + row_idx * 88
        for col_idx, ch in enumerate(line):
            x = 42 + col_idx * 65
            dr.text((x, y), ch, fill=ink_rgb, font=f)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path)
    return "".join(lines)


def main() -> None:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    bank = extract_font_glyph_bank("/System/Library/Fonts/Noteworthy.ttc", font_size=108)
    print(f"Extracted Noteworthy glyph bank: {len(bank)} glyphs")

    # Save compact real handwritten glyph bank for JS & Python
    (ROOT / "training" / "real_handwriting_bank.json").write_text(
        json.dumps(bank, separators=(",", ":"))
    )

    sheets = [
        ("/System/Library/Fonts/Noteworthy.ttc", SAMPLES_DIR / "sample-notebook.png", (252, 250, 244), (22, 24, 30)),
        ("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf", SAMPLES_DIR / "sample-architect.png", (246, 249, 253), (18, 32, 58)),
        ("/System/Library/Fonts/MarkerFelt.ttc", SAMPLES_DIR / "sample-marker.png", (253, 251, 245), (28, 22, 20)),
        ("/System/Library/Fonts/Supplemental/Chalkboard.ttc", SAMPLES_DIR / "sample-chalkboard.png", (249, 248, 242), (30, 30, 34)),
    ]
    for fp, out_p, paper, ink in sheets:
        render_handwriting_sample_sheet(fp, out_p, paper_rgb=paper, ink_rgb=ink)
        print(f"Rendered sample handwriting sheet: {out_p} ({out_p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
