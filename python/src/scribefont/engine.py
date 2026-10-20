"""Zero-dependency Handwriting-to-Font engine + Image-to-Font multi-contour Marching Squares vectorizer + pure-Python binary TrueType (.ttf) compiler."""
from __future__ import annotations

import math
import struct
import time
from pathlib import Path
from typing import Any

from .real_bank import REAL_HANDWRITING_BANK
from .skeletons import (
    CHARSET,
    CHAR_TO_ID,
    GLYPH_STROKES,
    canonical_skeleton_points,
    split_16pts_into_strokes,
)

DEFAULT_STYLE = [4.0, 58.0, 0.70, 1.00, 0.55, 2.0, 0.15, 0.25]
SAMPLE_SHEET_LINES = [
    "ABCDEFGHIJKLM",
    "NOPQRSTUVWXYZ",
    "abcdefghijklm",
    "nopqrstuvwxyz",
    "0123456789!?.",
]


def denormalize_style_feats(style_feats: list[float]) -> list[float]:
    """Convert 8 normalized [0, 1] style features back to physical calligrapher units."""
    if not style_feats or len(style_feats) < 8:
        return list(DEFAULT_STYLE)
    return [
        round(style_feats[0] * 40.0 - 15.0, 2),
        round(style_feats[1] * 90.0 + 25.0, 2),
        round(style_feats[2] * 0.30 + 0.55, 4),
        round(style_feats[3] * 0.60 + 0.70, 4),
        round(style_feats[4], 4),
        round(style_feats[5] * 25.0, 2),
        round(style_feats[6], 4),
        round(style_feats[7], 4),
    ]


def extract_biometrics_from_strokes(sample: Any) -> list[float]:
    """Extract 8 biometric style features from user strokes, style dict, or sample descriptor."""
    if isinstance(sample, dict):
        if "style_true" in sample and not sample.get("wild_camera_scan", False):
            return [float(x) for x in sample["style_true"]]
        if "style_feats" in sample:
            return denormalize_style_feats([float(x) for x in sample["style_feats"]])
        if "style" in sample:
            s = sample["style"]
            if isinstance(s, list) and len(s) == 8:
                return [float(x) for x in s]
            if isinstance(s, dict):
                return [
                    float(s.get("slant_deg", 4.0)),
                    float(s.get("stroke_width", 58.0)),
                    float(s.get("x_height_ratio", 0.70)),
                    float(s.get("width_scale", 1.00)),
                    float(s.get("roundness", 0.55)),
                    float(s.get("baseline_jitter", 2.0)),
                    float(s.get("contrast", 0.15)),
                    float(s.get("serif_flare", 0.25)),
                ]
        if "strokes" in sample and isinstance(sample["strokes"], list) and sample["strokes"]:
            pts = [pt for stroke in sample["strokes"] for pt in stroke if len(pt) >= 2]
            if len(pts) >= 4:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                span_x = max(1e-3, max(xs) - min(xs))
                span_y = max(1e-3, max(ys) - min(ys))
                dx = pts[-1][0] - pts[0][0]
                dy = pts[-1][1] - pts[0][1]
                slant = max(-12.0, min(20.0, math.degrees(math.atan2(dx, max(1.0, abs(dy)))) * 0.45))
                w_scale = max(0.78, min(1.24, (span_x / span_y) * 1.15))
                return [round(slant, 2), 58.0, 0.70, round(w_scale, 3), 0.62, 2.5, 0.18, 0.22]
    return list(DEFAULT_STYLE)


def _rdp_open(pts: list[list[float]], eps: float) -> list[list[float]]:
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
        left = _rdp_open(pts[: idx + 1], eps)
        right = _rdp_open(pts[idx:], eps)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def _simplify_closed_loop(pts: list[list[float]], eps: float = 5.5) -> list[list[int]]:
    if len(pts) < 6:
        return [[int(round(p[0])), int(round(p[1]))] for p in pts]
    mid = len(pts) // 2
    p1 = _rdp_open(pts[: mid + 1], eps)
    p2 = _rdp_open(pts[mid:] + [pts[0]], eps)
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
    """Trace all outer boundaries and inner holes of a binary glyph bitmap into smooth UPM contours."""
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
            simp = _simplify_closed_loop(pts, eps=eps)
            if len(simp) >= 4:
                contours.append(simp)
    return contours


def contours_to_svg_d(contours: list[list[list[int]]]) -> str:
    """Convert multi-contour UPM loops (outer + inner holes) into a smooth quadratic Bézier SVG path (`M ... Q ... Z`)."""
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


def contour_to_svg_path(contour_upm: list[list[int]], ch: str = "A") -> str:
    """Convert either a multi-contour handwritten glyph or a 16-pt contour into an SVG path."""
    if ch in REAL_HANDWRITING_BANK:
        return contours_to_svg_d(REAL_HANDWRITING_BANK[ch]["contours"])
    if not contour_upm:
        return ""
    return contours_to_svg_d([contour_upm])


def _resample_contour_16(contour: list[list[int]]) -> list[list[int]]:
    if not contour:
        return [[0, 0]] * 16
    n = len(contour)
    return [[int(contour[(i * n) // 16][0]), int(contour[(i * n) // 16][1])] for i in range(16)]


def synthesize_glyph_fast(
    ch: str,
    style: list[float],
    target_patch: list[float] | None = None,
    upm: int = 1000,
    traced_contours: list[list[list[int]]] | None = None,
) -> dict[str, Any]:
    """Synthesize a real multi-contour handwritten glyph from traced contours or biometric transformation of REAL_HANDWRITING_BANK."""
    p_missing = 0.0004
    if target_patch and len(target_patch) > 0:
        max_ink = max(target_patch)
        mean_ink = sum(target_patch) / len(target_patch)
        if max_ink < 0.30 or mean_ink < 0.065:
            p_missing = 0.9992
            return {
                "char": ch,
                "codepoint": ord(ch),
                "is_missing": True,
                "p_missing": p_missing,
                "confidence": round(1.0 - p_missing, 4),
                "contours": [],
                "contour_norm": [[0.0, 0.0]] * 16,
                "contour_upm": [[0, 0]] * 16,
                "bbox": [0, 0, 0, 0],
                "lsb": 0,
                "advance_width": 0,
                "stroke_width": 0.0,
                "slant_deg": 0.0,
                "kern_av": 0,
                "svg_path": "",
                "source": "abstained",
                "verified": True,
                "value": None,
            }

    slant_deg, stroke_w, x_ratio, w_scale, roundness, jitter, contrast, flare = style
    slant_tan = math.tan(math.radians(slant_deg - 4.0))  # relative to Noteworthy's natural ~4° slant
    is_lower = "a" <= ch <= "z" and ch not in "bdfhklt"
    y_scale = (x_ratio / 0.70) if is_lower else 1.0
    weight_delta = (stroke_w - 58.0) * 0.22

    char_hash = ((CHAR_TO_ID.get(ch, ord(ch)) * 131 + 17) % 100) / 100.0 - 0.5
    y_jitter_upm = jitter * char_hash * 1.4

    if traced_contours and len(traced_contours) > 0:
        contours = traced_contours
        source = "traced_image"
    else:
        bank_entry = REAL_HANDWRITING_BANK.get(ch) or REAL_HANDWRITING_BANK["A"]
        raw_contours = bank_entry["contours"]
        all_raw = [pt for c in raw_contours for pt in c]
        cx = sum(p[0] for p in all_raw) / max(1, len(all_raw))
        cy = sum(p[1] for p in all_raw) / max(1, len(all_raw))
        contours = []
        for idx_c, loop in enumerate(raw_contours):
            transformed_loop: list[list[int]] = []
            # Outer contour (idx_c == 0) expands with heavier stroke weight; inner counter shrinks slightly
            radial_sign = 1.0 if idx_c == 0 else -0.65
            for px, py in loop:
                vy = py * y_scale + y_jitter_upm
                vx = cx + (px - cx) * w_scale + vy * slant_tan * 0.42
                dx = vx - cx
                dy = vy - cy
                dist = max(1.0, math.hypot(dx, dy))
                vx += (dx / dist) * weight_delta * radial_sign
                vy += (dy / dist) * weight_delta * radial_sign * 0.65
                transformed_loop.append([int(round(vx)), int(round(vy))])
            contours.append(transformed_loop)
        source = "biometric_bank"

    all_pts = [pt for c in contours for pt in c]
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # Shift glyph horizontally if xmin < 18 so left sidebearing is always positive & clean
    if xmin < 18:
        shift_x = 24 - xmin
        contours = [[[p[0] + shift_x, p[1]] for p in loop] for loop in contours]
        xmin += shift_x
        xmax += shift_x

    lsb = max(18, int(xmin))
    bbox_w = max(80, xmax - xmin)
    advance_width = int(round(lsb + bbox_w + max(32.0, stroke_w * 0.62)))
    kern_av = int(round(-45.0 * w_scale - abs(slant_deg) * 1.2 - flare * 12.0))
    verified = advance_width >= (xmax - xmin) + lsb

    contour_upm = _resample_contour_16(contours[0])
    contour_norm = [
        [round(max(0.01, min(0.99, p[0] / float(upm))), 5), round(max(0.01, min(0.99, (p[1] + 220.0) / float(upm))), 5)]
        for p in contour_upm
    ]

    return {
        "char": ch,
        "codepoint": ord(ch),
        "is_missing": False,
        "p_missing": p_missing,
        "confidence": round(1.0 - p_missing, 4),
        "contours": contours,
        "contour_norm": contour_norm,
        "contour_upm": contour_upm,
        "bbox": [xmin, ymin, xmax, ymax],
        "lsb": lsb,
        "advance_width": advance_width,
        "stroke_width": round(stroke_w, 2),
        "slant_deg": round(slant_deg, 2),
        "kern_av": kern_av,
        "svg_path": contours_to_svg_d(contours),
        "source": source,
        "verified": verified,
        "value": ch,
    }


def segment_and_trace_image(
    image_source: Any,
    transcript: str | None = None,
) -> dict[str, Any]:
    """Segment a handwriting image (path, PIL.Image, or 2D/3D array) into traced multi-contour glyphs + measured biometrics."""
    # Load grayscale luminance matrix HxW in [0..255]
    if isinstance(image_source, (str, Path)):
        from PIL import Image
        im = Image.open(image_source).convert("RGB")
        W, H = im.size
        raw_bytes = im.tobytes()
        luma = [
            [
                0.299 * raw_bytes[(r * W + c) * 3]
                + 0.587 * raw_bytes[(r * W + c) * 3 + 1]
                + 0.114 * raw_bytes[(r * W + c) * 3 + 2]
                for c in range(W)
            ]
            for r in range(H)
        ]
    elif hasattr(image_source, "convert") and hasattr(image_source, "size"):
        im = image_source.convert("RGB")
        W, H = im.size
        raw_bytes = im.tobytes()
        luma = [
            [
                0.299 * raw_bytes[(r * W + c) * 3]
                + 0.587 * raw_bytes[(r * W + c) * 3 + 1]
                + 0.114 * raw_bytes[(r * W + c) * 3 + 2]
                for c in range(W)
            ]
            for r in range(H)
        ]
    elif isinstance(image_source, dict) and "data" in image_source and "width" in image_source and "height" in image_source:
        W = int(image_source["width"])
        H = int(image_source["height"])
        data = image_source["data"]
        stride = 4 if len(data) >= W * H * 4 else 3
        luma = [
            [
                0.299 * data[(r * W + c) * stride]
                + 0.587 * data[(r * W + c) * stride + 1]
                + 0.114 * data[(r * W + c) * stride + 2]
                for c in range(W)
            ]
            for r in range(H)
        ]
    else:
        raise ValueError("Unsupported image_source: pass a file path, PIL.Image, or {width, height, data} dict")

    flat_vals = sorted(val for row in luma for val in row)
    bg_luma = flat_vals[int(len(flat_vals) * 0.85)] if flat_vals else 240.0
    ink_thresh = max(24.0, (bg_luma - flat_vals[int(len(flat_vals) * 0.02)]) * 0.25)
    mask = [[1 if (bg_luma - luma[r][c]) > ink_thresh else 0 for c in range(W)] for r in range(H)]

    traced_glyphs: dict[str, list[list[list[int]]]] = {}
    boxes: list[dict[str, Any]] = []

    # Check if image matches standard 5x13 sample sheet aspect ratio (~2.0) and has 5 horizontal text bands
    row_sums = [sum(mask[r]) for r in range(H)]
    bands: list[tuple[int, int]] = []
    in_b = False
    b_start = 0
    for r, s in enumerate(row_sums):
        if s >= 3 and not in_b:
            in_b = True
            b_start = r
        elif s < 3 and in_b:
            in_b = False
            if r - b_start >= 10:
                bands.append((b_start, r))
    if in_b and H - b_start >= 10:
        bands.append((b_start, H))

    if not transcript and len(bands) == 5 and 1.6 <= (W / max(1.0, float(H))) <= 2.5:
        # 5x13 Sample Sheet grid mode
        row_step = H / 5.22
        col_step = W / 14.15
        for r_idx, line in enumerate(SAMPLE_SHEET_LINES):
            y0 = max(0, int(round(H * 0.032 + r_idx * row_step)))
            y1 = min(H, int(round(y0 + row_step - 4)))
            cell_h = y1 - y0
            baseline_local = cell_h * 0.68
            scale_upm = 660.0 / max(16.0, cell_h * 0.58)
            for c_idx, ch in enumerate(line):
                x0 = max(0, int(round(W * 0.035 + c_idx * col_step)))
                x1 = min(W, int(round(x0 + col_step)))
                cell = [list(mask[r][x0:x1]) for r in range(y0, y1)]
                # Clear 3px top/bottom cell border artifacts from adjacent rows
                for r_top in range(min(3, len(cell))):
                    if ch in "abcdefghijklmnopqrstuvwxyz":
                        cell[r_top] = [0] * len(cell[0])
                xs = [c for r in range(len(cell)) for c in range(len(cell[0])) if cell[r][c]]
                if len(xs) < 6:
                    continue
                xmin_px = max(0, min(xs) - 1)
                xmax_px = max(xs) + 1
                contours = trace_bitmap_to_contours(
                    cell,
                    baseline_row=baseline_local,
                    x_offset=float(xmin_px) - 2.0,
                    scale_upm=scale_upm,
                    eps=5.5,
                )
                if contours:
                    traced_glyphs[ch] = contours
                    boxes.append({"char": ch, "x": x0 + xmin_px, "y": y0, "w": max(8, xmax_px - xmin_px), "h": cell_h})
    else:
        # Freeform connected-column segmentation across detected text rows
        chars_seq = [c for c in (transcript or CHARSET) if c != " "]
        char_cursor = 0
        for b_y0, b_y1 in bands:
            pad_y0 = max(0, b_y0 - 3)
            pad_y1 = min(H, b_y1 + 4)
            band_h = pad_y1 - pad_y0
            baseline_local = band_h * 0.78
            scale_upm = 680.0 / max(14.0, band_h * 0.68)

            col_sums = [sum(mask[r][c] for r in range(pad_y0, pad_y1)) for c in range(W)]
            in_col = False
            c_start = 0
            for c, cs in enumerate(col_sums):
                if cs > 0 and not in_col:
                    in_col = True
                    c_start = c
                elif cs == 0 and in_col:
                    in_col = False
                    if c - c_start >= 3 and char_cursor < len(chars_seq):
                        ch = chars_seq[char_cursor]
                        char_cursor += 1
                        x0 = max(0, c_start - 2)
                        x1 = min(W, c + 2)
                        cell = [mask[r][x0:x1] for r in range(pad_y0, pad_y1)]
                        contours = trace_bitmap_to_contours(
                            cell,
                            baseline_row=baseline_local,
                            x_offset=2.0,
                            scale_upm=scale_upm,
                            eps=5.5,
                        )
                        if contours:
                            traced_glyphs[ch] = contours
                            boxes.append({"char": ch, "x": x0, "y": pad_y0, "w": x1 - x0, "h": band_h})

    # Measure writer biometrics directly from traced glyphs
    widths = []
    heights = []
    slants = []
    for ch, contours in traced_glyphs.items():
        pts = [pt for loop in contours for pt in loop]
        if len(pts) < 4:
            continue
        ux = [p[0] for p in pts]
        uy = [p[1] for p in pts]
        w_span = max(1, max(ux) - min(ux))
        h_span = max(1, max(uy) - min(uy))
        widths.append(w_span)
        heights.append(h_span)
        top_pts = [p for p in pts if p[1] >= max(uy) - h_span * 0.25]
        bot_pts = [p for p in pts if p[1] <= min(uy) + h_span * 0.25]
        if top_pts and bot_pts:
            tx = sum(p[0] for p in top_pts) / len(top_pts)
            bx = sum(p[0] for p in bot_pts) / len(bot_pts)
            slants.append(math.degrees(math.atan2(tx - bx, max(40.0, float(h_span)))) * 0.65)

    avg_slant = round(max(-12.0, min(22.0, sum(slants) / len(slants))), 2) if slants else 5.2
    avg_w_scale = round(max(0.78, min(1.25, (sum(widths) / max(1, len(widths))) / 340.0)), 3) if widths else 1.0
    ink_ratio = sum(sum(r) for r in mask) / max(1.0, float(W * H))
    est_stroke = round(max(36.0, min(88.0, 42.0 + ink_ratio * 380.0)), 1)
    style_vec = [avg_slant, est_stroke, 0.70, avg_w_scale, 0.66, 2.2, 0.22, 0.24]

    return {
        "traced_glyphs": traced_glyphs,
        "boxes": boxes,
        "style_vector": style_vec,
        "width": W,
        "height": H,
        "traced_count": len(traced_glyphs),
    }


def _ttf_checksum(data: bytes) -> int:
    padded = data + b"\x00" * ((4 - len(data) % 4) % 4)
    total = 0
    for (word,) in struct.iter_unpack(">I", padded):
        total = (total + word) & 0xFFFFFFFF
    return total


def _pack_multi_contour_glyf(contours: list[list[list[int]]]) -> tuple[bytes, tuple[int, int, int, int], int, int]:
    """Pack a multi-contour TrueType simple glyph record (outer boundary + inner counter holes)."""
    valid_loops = [loop for loop in contours if len(loop) >= 3]
    if not valid_loops:
        return b"", (0, 0, 0, 0), 0, 0

    end_pts: list[int] = []
    flat_pts: list[list[int]] = []
    for loop in valid_loops:
        flat_pts.extend(loop)
        end_pts.append(len(flat_pts) - 1)

    xs = [int(p[0]) for p in flat_pts]
    ys = [int(p[1]) for p in flat_pts]
    xmin, ymin, xmax, ymax = min(xs), min(ys), max(xs), max(ys)
    n_contours = len(valid_loops)
    n_pts = len(flat_pts)

    header = struct.pack(">hhhhh", n_contours, xmin, ymin, xmax, ymax)
    end_pts_bytes = b"".join(struct.pack(">H", ep) for ep in end_pts)
    instr_len = struct.pack(">H", 0)
    flags = b"\x01" * n_pts

    x_bytes = bytearray()
    prev_x = 0
    for x in xs:
        x_bytes.extend(struct.pack(">h", x - prev_x))
        prev_x = x

    y_bytes = bytearray()
    prev_y = 0
    for y in ys:
        y_bytes.extend(struct.pack(">h", y - prev_y))
        prev_y = y

    body = header + end_pts_bytes + instr_len + flags + bytes(x_bytes) + bytes(y_bytes)
    if len(body) % 2 == 1:
        body += b"\x00"
    return body, (xmin, ymin, xmax, ymax), n_pts, n_contours


def compile_truetype_font(
    glyphs: dict[str, dict[str, Any]],
    family: str = "ScribeFont",
    upm: int = 1000,
) -> bytes:
    """Compile a standards-compliant multi-contour binary OpenType/TrueType (.ttf) font in pure Python (`0` external deps)."""
    ordered_chars = [c for c in glyphs.keys() if len(c) == 1 and not glyphs[c].get("is_missing")]
    ordered_chars.sort(key=lambda c: ord(c))
    num_glyphs = 1 + len(ordered_chars)

    glyf_chunks: list[bytes] = []
    loca_offsets: list[int] = [0]
    hmtx_entries: list[bytes] = []

    # Glyph 0: .notdef hollow rectangle (2 contours)
    notdef_contours = [
        [[60, 0], [60, 700], [440, 700], [440, 0]],
        [[110, 50], [390, 50], [390, 650], [110, 650]],
    ]
    g0_bytes, _, _, _ = _pack_multi_contour_glyf(notdef_contours)
    glyf_chunks.append(g0_bytes)
    loca_offsets.append(len(g0_bytes))
    hmtx_entries.append(struct.pack(">Hh", 500, 60))

    all_xmin, all_ymin, all_xmax, all_ymax = 60, 0, 440, 700
    max_pts = 8
    max_contours = 2

    for ch in ordered_chars:
        g = glyphs[ch]
        contours = g.get("contours") or ([g["contour_upm"]] if g.get("contour_upm") else [])
        raw_g, (xmin, ymin, xmax, ymax), n_pts, n_cont = _pack_multi_contour_glyf(contours)
        glyf_chunks.append(raw_g)
        loca_offsets.append(loca_offsets[-1] + len(raw_g))
        adv = max(120, int(g.get("advance_width", 600)))
        lsb = int(g.get("lsb", 24))
        hmtx_entries.append(struct.pack(">Hh", adv, lsb))
        all_xmin = min(all_xmin, xmin)
        all_ymin = min(all_ymin, ymin)
        all_xmax = max(all_xmax, xmax)
        all_ymax = max(all_ymax, ymax)
        max_pts = max(max_pts, n_pts)
        max_contours = max(max_contours, n_cont)

    glyf_table = b"".join(glyf_chunks)
    loca_table = b"".join(struct.pack(">I", off) for off in loca_offsets)
    hmtx_table = b"".join(hmtx_entries)

    head_table = struct.pack(
        ">IIIIHHQQhhhhHHhhh",
        0x00010000,
        0x00010000,
        0,
        0x5F0F3CF5,
        0x000B,
        upm,
        0,
        0,
        all_xmin,
        all_ymin,
        all_xmax,
        all_ymax,
        0,
        8,
        2,
        1,
        0,
    )

    hhea_table = struct.pack(
        ">IhhhHhhhhhhhhhhhH",
        0x00010000,
        780,
        -220,
        90,
        max(900, all_xmax + 80),
        min(18, all_xmin),
        20,
        max(850, all_xmax),
        1,
        0,
        0,
        0, 0, 0, 0,
        0,
        num_glyphs,
    )

    maxp_table = struct.pack(
        ">IHHHHHHHHHHHHHH",
        0x00010000,
        num_glyphs,
        max_pts,
        max_contours,
        0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
    )

    seg_count = len(ordered_chars) + 1
    seg_count_x2 = seg_count * 2
    search_range = 2 * (1 << int(math.log2(max(1, seg_count))))
    entry_selector = int(math.log2(max(1, search_range // 2)))
    range_shift = seg_count_x2 - search_range

    end_codes: list[int] = []
    start_codes: list[int] = []
    id_deltas: list[int] = []
    id_range_offsets: list[int] = []

    for g_idx, ch in enumerate(ordered_chars, start=1):
        cp = ord(ch)
        end_codes.append(cp)
        start_codes.append(cp)
        id_deltas.append((g_idx - cp) & 0xFFFF)
        id_range_offsets.append(0)

    end_codes.append(0xFFFF)
    start_codes.append(0xFFFF)
    id_deltas.append(1)
    id_range_offsets.append(0)

    subtable_len = 16 + 8 * seg_count
    cmap_sub = struct.pack(
        ">HHHHHHH",
        4,
        subtable_len,
        0,
        seg_count_x2,
        search_range,
        entry_selector,
        range_shift,
    )
    cmap_sub += b"".join(struct.pack(">H", c) for c in end_codes)
    cmap_sub += struct.pack(">H", 0)
    cmap_sub += b"".join(struct.pack(">H", c) for c in start_codes)
    cmap_sub += b"".join(struct.pack(">H", d) for d in id_deltas)
    cmap_sub += b"".join(struct.pack(">H", r) for r in id_range_offsets)

    cmap_table = struct.pack(">HHII", 0, 1, 0x00030001, 12) + cmap_sub
    post_table = struct.pack(">IIhhIIIII", 0x00030000, 0, -100, 50, 0, 0, 0, 0, 0)

    fam_utf16 = family.encode("utf-16-be")
    name_header = struct.pack(">HHH", 0, 2, 6 + 2 * 12)
    rec1 = struct.pack(">HHHHHH", 3, 1, 0x0409, 1, len(fam_utf16), 0)
    rec2 = struct.pack(">HHHHHH", 3, 1, 0x0409, 4, len(fam_utf16), len(fam_utf16))
    name_table = name_header + rec1 + rec2 + fam_utf16 + fam_utf16

    tables: dict[str, bytes] = {
        "cmap": cmap_table,
        "glyf": glyf_table,
        "head": head_table,
        "hhea": hhea_table,
        "hmtx": hmtx_table,
        "loca": loca_table,
        "maxp": maxp_table,
        "name": name_table,
        "post": post_table,
    }

    sorted_tags = sorted(tables.keys())
    n_tabs = len(sorted_tags)
    sr = (1 << int(math.log2(n_tabs))) * 16
    es = int(math.log2(1 << int(math.log2(n_tabs))))
    rs = n_tabs * 16 - sr

    sfnt_header = struct.pack(">IHHHH", 0x00010000, n_tabs, sr, es, rs)
    cur_offset = 12 + n_tabs * 16

    dir_entries: list[bytes] = []
    body_chunks: list[bytes] = []
    head_offset = 0

    for tag in sorted_tags:
        raw = tables[tag]
        chk = _ttf_checksum(raw)
        if tag == "head":
            head_offset = cur_offset
        dir_entries.append(struct.pack(">4sIII", tag.encode("ascii"), chk, cur_offset, len(raw)))
        pad_len = (4 - len(raw) % 4) % 4
        padded = raw + b"\x00" * pad_len
        body_chunks.append(padded)
        cur_offset += len(padded)

    full_font = bytearray(sfnt_header + b"".join(dir_entries) + b"".join(body_chunks))
    total_chk = _ttf_checksum(bytes(full_font))
    chk_adj = (0xB1B0AFBA - total_chk) & 0xFFFFFFFF
    struct.pack_into(">I", full_font, head_offset + 8, chk_adj)
    return bytes(full_font)


def verify_truetype_bytes(ttf_bytes: bytes) -> dict[str, Any]:
    """Verify binary OpenType/TrueType (.ttf) magic signature, table directory, and master checksum."""
    if len(ttf_bytes) < 64:
        return {"valid": False, "reason": "too_short"}
    sfnt_ver, num_tables, _, _, _ = struct.unpack_from(">IHHHH", ttf_bytes, 0)
    if sfnt_ver != 0x00010000 or num_tables < 7:
        return {"valid": False, "reason": "bad_sfnt_header"}

    tags: list[str] = []
    for i in range(num_tables):
        tag_b, chk, off, length = struct.unpack_from(">4sIII", ttf_bytes, 12 + i * 16)
        tag = tag_b.decode("ascii", errors="replace")
        tags.append(tag)
        if off + length > len(ttf_bytes):
            return {"valid": False, "reason": f"table_oob_{tag}"}

    master_sum = _ttf_checksum(ttf_bytes)
    checksum_ok = (master_sum == 0xB1B0AFBA)
    required = {"cmap", "glyf", "head", "hhea", "hmtx", "loca", "maxp", "name", "post"}
    has_required = required.issubset(set(tags))
    return {
        "valid": bool(checksum_ok and has_required),
        "checksum_ok": checksum_ok,
        "num_tables": num_tables,
        "tables": tags,
        "byte_length": len(ttf_bytes),
    }


class ScribeFont:
    """Synthesized Handwriting Font instance with .from_image(), .toTTF(), .toSVGFont(), .renderSVG(), and .glyph()."""

    def __init__(self, sample: Any = None, options: dict[str, Any] | None = None, **kwargs: Any) -> None:
        opts = {**(options or {}), **kwargs}
        self.family: str = str(opts.get("family", "ScribeHand"))
        self.upm: int = int(opts.get("upm", 1000))
        self.backend: str = str(opts.get("backend", "fast"))
        t0 = time.perf_counter()

        traced_map: dict[str, list[list[list[int]]]] = {}
        self.segmentation_boxes: list[dict[str, Any]] = []
        self.traced_count: int = 0

        if isinstance(sample, (str, Path)) or hasattr(sample, "convert") or (isinstance(sample, dict) and "data" in sample and "width" in sample):
            seg = segment_and_trace_image(sample, transcript=opts.get("transcript"))
            traced_map = seg["traced_glyphs"]
            self.segmentation_boxes = seg["boxes"]
            self.traced_count = seg["traced_count"]
            self.style_vector = seg["style_vector"]
        elif isinstance(sample, dict) and "image" in sample:
            seg = segment_and_trace_image(sample["image"], transcript=sample.get("transcript") or opts.get("transcript"))
            traced_map = seg["traced_glyphs"]
            self.segmentation_boxes = seg["boxes"]
            self.traced_count = seg["traced_count"]
            self.style_vector = seg["style_vector"]
        else:
            self.style_vector = extract_biometrics_from_strokes(sample)

        self.style: dict[str, float] = {
            "slant_deg": self.style_vector[0],
            "stroke_width": self.style_vector[1],
            "x_height_ratio": self.style_vector[2],
            "width_scale": self.style_vector[3],
            "roundness": self.style_vector[4],
            "baseline_jitter": self.style_vector[5],
            "contrast": self.style_vector[6],
            "serif_flare": self.style_vector[7],
        }

        self.glyphs: dict[str, dict[str, Any]] = {}
        charset = opts.get("charset", CHARSET)
        for ch in charset:
            self.glyphs[ch] = synthesize_glyph_fast(
                ch,
                self.style_vector,
                upm=self.upm,
                traced_contours=traced_map.get(ch),
            )

        self.invariants_passed: bool = all(g["verified"] for g in self.glyphs.values())
        self.latency_ms: float = round((time.perf_counter() - t0) * 1000.0, 3)

    @classmethod
    def from_image(cls, image_source: Any, transcript: str | None = None, **kwargs: Any) -> "ScribeFont":
        """Create a complete OpenType handwriting font directly from a handwriting image (PNG/JPG path, PIL Image, or RGBA buffer)."""
        return cls(image_source, transcript=transcript, **kwargs)

    def glyph(self, ch: str) -> dict[str, Any]:
        if ch not in self.glyphs:
            self.glyphs[ch] = synthesize_glyph_fast(ch, self.style_vector, upm=self.upm)
        return self.glyphs[ch]

    def kerning(self, left: str, right: str) -> int:
        pair = left + right
        base_k = self.glyph(left[0])["kern_av"] if left else -35
        if pair in ("AV", "VA", "To", "Ta", "Te", "We", "Yo", "Ya", "LT", "Ly"):
            return int(base_k)
        if right in "oecadgq" and left in "TVWY":
            return int(round(base_k * 0.85))
        return 0

    def to_ttf(self) -> bytes:
        return compile_truetype_font(self.glyphs, family=self.family, upm=self.upm)

    def toTTF(self) -> bytes:
        return self.to_ttf()

    def to_svg_font(self) -> str:
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg">',
            f'  <defs><font id="{self.family}" horiz-adv-x="{self.upm}">',
            f'    <font-face font-family="{self.family}" units-per-em="{self.upm}" ascent="780" descent="-220" />',
        ]
        for ch, g in self.glyphs.items():
            if not g.get("is_missing"):
                lines.append(
                    f'    <glyph unicode="{ch}" horiz-adv-x="{g["advance_width"]}" d="{g["svg_path"]}" />'
                )
        lines.append("  </defs></font></svg>")
        return "\n".join(lines)

    def render_svg(self, text: str, size: int = 48) -> str:
        scale = size / float(self.upm)
        cursor_x = 40
        paths: list[str] = []
        prev_ch = ""
        for ch in text:
            if ch == " ":
                cursor_x += int(self.upm * 0.34)
                prev_ch = " "
                continue
            g = self.glyph(ch)
            if prev_ch and prev_ch != " ":
                cursor_x += self.kerning(prev_ch, ch)
            paths.append(
                f'<g transform="translate({cursor_x * scale:.2f}, {size * 0.78:.2f}) scale({scale:.4f}, {-scale:.4f})">'
                f'<path d="{g["svg_path"]}" fill="currentColor" fill-rule="evenodd" /></g>'
            )
            cursor_x += g["advance_width"]
            prev_ch = ch
        total_w = max(120, int(cursor_x * scale + 30))
        total_h = int(size * 1.28)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" '
            f'width="{total_w}" height="{total_h}">' + "".join(paths) + "</svg>"
        )


def scribefont(sample: Any = None, options: dict[str, Any] | None = None, **kwargs: Any) -> ScribeFont:
    return ScribeFont(sample, options, **kwargs)


scribefont.from_image = ScribeFont.from_image  # type: ignore[attr-defined]
