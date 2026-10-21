#!/usr/bin/env python3
"""
Extract authentic handwritten Devanagari / Sanskrit (U+0901..U+097F) and Indic
(Kannada, Tamil, Telugu, Bengali) glyph contours in 1000-UPM font coordinates.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
KALAM_PATH = Path("/tmp/Kalam-Regular.ttf")

# Full Devanagari & Sanskrit character inventory (80+ codepoints)
DEVANAGARI_VOWELS = "अआइईउऊऋॠऌएऐओऔ"
DEVANAGARI_CONSONANTS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलळवशषसह"
DEVANAGARI_MATRAS_SPACING = "ाीोौः"
DEVANAGARI_MATRA_PRE = "ि"
DEVANAGARI_MATRAS_ABOVE = "ेैंँॅ"
DEVANAGARI_MATRAS_BELOW = "ुूृॄ़्"
DEVANAGARI_SANSKRIT_SPECIALS = "ॐऽ।॥"
DEVANAGARI_DIGITS = "०१२३४५६७८९"

DEVANAGARI_CHARSET = (
    DEVANAGARI_VOWELS
    + DEVANAGARI_CONSONANTS
    + DEVANAGARI_MATRAS_SPACING
    + DEVANAGARI_MATRA_PRE
    + DEVANAGARI_MATRAS_ABOVE
    + DEVANAGARI_MATRAS_BELOW
    + DEVANAGARI_SANSKRIT_SPECIALS
    + DEVANAGARI_DIGITS
)

# Core Indic scripts (Kannada, Tamil, Telugu, Bengali) for multilingual studio & font synthesis
KANNADA_CHARS = "अआकगचजटडतदनपबमयरलवशसह"  # mapped below to Kannada block
KANNADA_SET = "ಅಆಇಈಉಊಋಎಏಐಒಓಔಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲಳವಶಷಸಹಾಿೀುೂೃೆೇೈೊೋೌಂಃ್೦೧೨೩೪೫೬೭೮೯"
TAMIL_SET = "அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவழளறனஸஹாிீுூெேைொோௌ்ஃ௦௧௨௩௪௫௬௭௮௯"
TELUGU_SET = "అఆఇఈఉఊఋఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలళవశషసహాిీుూృెేైొోౌంః్౦౧౨౩౪౫౬౭౮౯"
BENGALI_SET = "অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়়ািীুূৃেৈোৌংঃঁ্০১২৩৪৫৬৭৮৯"

NON_SPACING_ABOVE = set(DEVANAGARI_MATRAS_ABOVE) | {"ೇ", "ೈ", "ೆ", "ं", "ँ", "ं", "्"}
NON_SPACING_BELOW = set(DEVANAGARI_MATRAS_BELOW) | {"ು", "ೂ", "ೃ", "ு", "ூ", "ు", "ూ", "ృ", "ু", "ূ", "ৃ"}
NON_SPACING_ALL = (
    set(DEVANAGARI_MATRAS_ABOVE)
    | set(DEVANAGARI_MATRAS_BELOW)
    | {"्", "ं", "ँ", "ॆ", "ॅ", "़", "ु", "ू", "ृ", "ॄ", "े", "ै"}
    | {"ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "್"}
    | {"ு", "ூ", "्", "்"}
    | {"ు", "ూ", "ృ", "ె", "ే", "ై", "్"}
    | {"ু", "ূ", "ৃ", "ঁ", "্"}
)


def rdp_open(pts: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
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


def simplify_loop(pts: list[tuple[float, float]], eps: float = 5.0) -> list[list[int]]:
    if len(pts) < 6:
        return [[int(round(p[0])), int(round(p[1]))] for p in pts]
    mid = len(pts) // 2
    p1 = rdp_open(pts[: mid + 1], eps)
    p2 = rdp_open(pts[mid:] + [pts[0]], eps)
    res = p1[:-1] + p2[:-1]
    if len(res) < 4:
        step = max(1, len(pts) // 6)
        res = pts[::step]
    return [[int(round(p[0])), int(round(p[1]))] for p in res]


def trace_mask_to_contours(
    mask: np.ndarray,
    baseline_row: float,
    x_offset: float,
    scale_upm: float,
    eps: float = 4.8,
) -> list[list[list[int]]]:
    H, W = mask.shape
    adj: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def add_edge(x0: int, y0: int, x1: int, y1: int) -> None:
        adj.setdefault((x0, y0), []).append((x1, y1))

    for r in range(H):
        for c in range(W):
            if not mask[r, c]:
                continue
            if r == 0 or not mask[r - 1, c]:
                add_edge(c, r, c + 1, r)
            if c == W - 1 or not mask[r, c + 1]:
                add_edge(c + 1, r, c + 1, r + 1)
            if r == H - 1 or not mask[r + 1, c]:
                add_edge(c + 1, r + 1, c, r + 1)
            if c == 0 or not mask[r, c - 1]:
                add_edge(c, r + 1, c, r)

    contours: list[list[list[int]]] = []
    while adj:
        start_pt = next(iter(adj.keys()))
        cx, cy = start_pt
        loop: list[tuple[int, int]] = []
        while True:
            loop.append((cx, cy))
            nxts = adj.get((cx, cy))
            if not nxts:
                break
            nx, ny = nxts.pop()
            if not nxts:
                del adj[(cx, cy)]
            cx, cy = nx, ny
            if (cx, cy) == start_pt:
                break
        if len(loop) >= 8:
            pts = [((px - x_offset) * scale_upm, (baseline_row - py) * scale_upm) for px, py in loop]
            for _ in range(2):
                n = len(pts)
                pts = [
                    (
                        0.25 * pts[(i - 1) % n][0] + 0.5 * pts[i][0] + 0.25 * pts[(i + 1) % n][0],
                        0.25 * pts[(i - 1) % n][1] + 0.5 * pts[i][1] + 0.25 * pts[(i + 1) % n][1],
                    )
                    for i in range(n)
                ]
            simp = simplify_loop(pts, eps=eps)
            if len(simp) >= 4:
                contours.append(simp)
    return contours


def extract_glyph_from_font(
    ch: str,
    font: ImageFont.FreeTypeFont,
    is_non_spacing: bool = False,
    is_below: bool = False,
    is_above: bool = False,
) -> dict | None:
    W, H = 420, 360
    im = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(im)

    baseline_y = 230
    origin_x = 180
    draw.text((origin_x, baseline_y), ch, fill=255, font=font, anchor="ls")

    arr = np.array(im)
    mask = arr > 110
    if mask.sum() < 6:
        return None

    scale_upm = 5.2
    adv_px = float(font.getlength(ch))
    is_comb = is_non_spacing or (adv_px <= 1.0)

    contours = trace_mask_to_contours(
        mask,
        baseline_row=baseline_y,
        x_offset=origin_x,
        scale_upm=scale_upm,
        eps=4.2 if is_comb else 4.6,
    )
    if not contours:
        return None

    all_pts = [p for loop in contours for p in loop]
    ux_min = min(p[0] for p in all_pts)
    ux_max = max(p[0] for p in all_pts)

    if is_comb:
        # Ensure non-spacing mark overhangs left over the preceding base consonant if font placed it at x >= 0
        if ux_min >= -10:
            shift_left = -int(round(0.5 * (ux_min + ux_max) + 210))
            contours = [[[p[0] + shift_left, p[1]] for p in loop] for loop in contours]
            ux_min += shift_left
            ux_max += shift_left
        return {
            "contours": contours,
            "combining": True,
            "advance_width": 0,
            "lsb": int(round(ux_min)),
        }

    adv_upm = int(round(adv_px * scale_upm))
    if adv_upm < 140:
        adv_upm = int(round(max(180, (ux_max - ux_min) + 36)))
    return {
        "contours": contours,
        "combining": False,
        "advance_width": adv_upm,
        "lsb": int(round(ux_min)),
    }


def main() -> None:
    font_dev = ImageFont.truetype(str(KALAM_PATH), size=112, layout_engine=ImageFont.Layout.BASIC)
    bank: dict[str, dict] = {}

    for ch in DEVANAGARI_CHARSET:
        if len(ch) != 1:
            continue
        is_comb = ch in NON_SPACING_ALL
        is_above = ch in DEVANAGARI_MATRAS_ABOVE
        is_below = ch in DEVANAGARI_MATRAS_BELOW
        entry = extract_glyph_from_font(ch, font_dev, is_non_spacing=is_comb, is_below=is_below, is_above=is_above)
        if entry:
            bank[ch] = entry

    # Also extract core Kannada, Tamil, Telugu, Bengali characters
    indic_fonts = [
        (KANNADA_SET, "/System/Library/Fonts/NotoSansKannada.ttc"),
        (TAMIL_SET, "/System/Library/Fonts/Supplemental/Tamil Sangam MN.ttc"),
        (TELUGU_SET, "/System/Library/Fonts/KohinoorTelugu.ttc"),
        (BENGALI_SET, "/System/Library/Fonts/KohinoorBangla.ttc"),
    ]
    for charset_str, fpath in indic_fonts:
        if not Path(fpath).exists():
            continue
        f_obj = ImageFont.truetype(fpath, size=106, layout_engine=ImageFont.Layout.BASIC)
        for ch in charset_str:
            if len(ch) != 1 or ch in bank:
                continue
            is_comb = ch in NON_SPACING_ALL
            is_below = ch in NON_SPACING_BELOW
            is_above = ch in NON_SPACING_ABOVE and not is_below
            entry = extract_glyph_from_font(ch, f_obj, is_non_spacing=is_comb, is_below=is_below, is_above=is_above)
            if entry:
                bank[ch] = entry

    out_json = ROOT / "data" / "indic_handwriting_bank.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")))

    out_js = ROOT / "js" / "src" / "indic_bank.js"
    js_str = "export const INDIC_HANDWRITING_BANK = " + json.dumps(bank, ensure_ascii=False, separators=(",", ":")) + ";\n"
    out_js.write_text(js_str)
    (ROOT / "docs" / "src" / "indic_bank.js").write_text(js_str)

    out_py = ROOT / "python" / "src" / "scribefont" / "indic_bank.py"
    out_py.write_text("# Auto-generated Indic & Devanagari/Sanskrit handwritten vector bank\nINDIC_HANDWRITING_BANK = " + repr(bank) + "\n")

    print(f"Extracted {len(bank)} Indic & Devanagari/Sanskrit handwritten glyph contours ({out_js.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
