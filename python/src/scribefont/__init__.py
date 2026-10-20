"""scribefont — Single-pass Handwriting-to-Font synthesis, Image-to-Font multi-contour vectorizer & OpenType (.ttf) compiler."""
from __future__ import annotations

from .engine import (
    CHARSET,
    ScribeFont,
    canonical_skeleton_points,
    compile_truetype_font,
    contours_to_svg_d,
    denormalize_style_feats,
    scribefont,
    segment_and_trace_image,
    synthesize_glyph_fast,
    trace_bitmap_to_contours,
    verify_truetype_bytes,
)

__all__ = [
    "CHARSET",
    "ScribeFont",
    "canonical_skeleton_points",
    "compile_truetype_font",
    "contours_to_svg_d",
    "denormalize_style_feats",
    "scribefont",
    "segment_and_trace_image",
    "synthesize_glyph_fast",
    "trace_bitmap_to_contours",
    "verify_truetype_bytes",
]
__version__ = "0.2.0"
