"""scribefont — Single-pass Handwriting-to-Font synthesis & OpenType (.ttf) compiler."""
from __future__ import annotations

from .engine import (
    CHARSET,
    ScribeFont,
    canonical_skeleton_points,
    compile_truetype_font,
    denormalize_style_feats,
    scribefont,
    synthesize_glyph_fast,
    verify_truetype_bytes,
)

__all__ = [
    "CHARSET",
    "ScribeFont",
    "canonical_skeleton_points",
    "compile_truetype_font",
    "denormalize_style_feats",
    "scribefont",
    "synthesize_glyph_fast",
    "verify_truetype_bytes",
]
__version__ = "0.1.0"
