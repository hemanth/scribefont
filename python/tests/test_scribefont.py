"""Unit tests for scribefont Python engine, Image-to-Font vectorizer, and binary TrueType (.ttf) compiler."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from scribefont import (
    DEVANAGARI_CHARSET,
    INDIC_SCRIPTS,
    reorder_indic_visual_order,
    scribefont,
    synthesize_glyph_fast,
    verify_truetype_bytes,
)


class TestScribeFont(unittest.TestCase):
    def test_full_font_synthesis_and_ttf(self) -> None:
        font = scribefont(
            {
                "style": {
                    "slant_deg": 14.5,
                    "stroke_width": 52.0,
                    "x_height_ratio": 0.68,
                    "width_scale": 0.95,
                    "roundness": 0.78,
                    "baseline_jitter": 3.0,
                    "contrast": 0.45,
                    "serif_flare": 0.50,
                }
            },
            family="MiraScript",
        )
        self.assertEqual(font.family, "MiraScript")
        self.assertTrue(font.invariants_passed)
        self.assertGreaterEqual(len(font.glyphs), 62)

        g_a = font.glyph("A")
        self.assertFalse(g_a["is_missing"])
        self.assertLess(g_a["p_missing"], 0.01)
        self.assertGreaterEqual(len(g_a["contours"]), 2)  # outer + inner counter hole
        self.assertEqual(len(g_a["contour_upm"]), 16)
        self.assertTrue(g_a["svg_path"].startswith("M "))

        self.assertLess(font.kerning("A", "V"), -20)

        svg = font.render_svg("Hello Scribe 2026", size=48)
        self.assertIn("<svg", svg)
        self.assertIn("<path", svg)

        ttf_bytes = font.to_ttf()
        chk = verify_truetype_bytes(ttf_bytes)
        self.assertTrue(chk["valid"])
        self.assertTrue(chk["checksum_ok"])
        self.assertGreater(chk["byte_length"], 8000)

    def test_from_handwriting_image(self) -> None:
        sample_img = ROOT.parent / "docs" / "samples" / "sample-notebook.png"
        if sample_img.exists():
            font = scribefont.from_image(sample_img, family="NotebookHand")
            self.assertGreaterEqual(font.traced_count, 60)
            self.assertEqual(font.glyph("A")["source"], "traced_image")
            ttf_bytes = font.to_ttf()
            chk = verify_truetype_bytes(ttf_bytes)
            self.assertTrue(chk["valid"])
            self.assertTrue(chk["checksum_ok"])

    def test_from_internet_handwriting_images(self) -> None:
        """TDD: Real internet handwriting images (Palmer 1901, Mills 1909, School Alphabet) must segment >= 30 glyphs each."""
        internet_dir = ROOT.parent / "docs" / "samples" / "internet"
        for name in ("internet-palmer-1901.jpg", "internet-mills-1909.jpg", "internet-school-alphabet.jpg"):
            img_path = internet_dir / name
            self.assertTrue(img_path.exists(), f"Missing internet sample {img_path}")
            font = scribefont.from_image(img_path, family="InternetHand")
            self.assertGreaterEqual(font.traced_count, 30, f"{name} only traced {font.traced_count} glyphs")
            self.assertTrue(verify_truetype_bytes(font.to_ttf())["valid"])

    def test_from_canvas_strokes_and_bitmap(self) -> None:
        """TDD: Freehand canvas strokes via ScribeFont.from_canvas(...) must rasterize & trace real multi-contour glyphs."""
        self.assertTrue(hasattr(scribefont, "from_canvas"), "scribefont.from_canvas must exist")
        strokes = [
            # Letter 'A' drawn on canvas (outer legs + crossbar)
            [[24, 78], [44, 18], [64, 78]],
            [[31, 54], [57, 54]],
            # Letter 'B' drawn on canvas
            [[95, 18], [95, 78]],
            [[95, 18], [122, 22], [122, 45], [95, 48], [125, 54], [125, 75], [95, 78]],
        ]
        font = scribefont.from_canvas(strokes, width=220, height=96, transcript="AB", family="CanvasHand")
        self.assertGreaterEqual(font.traced_count, 2)
        self.assertEqual(font.glyph("A")["source"], "traced_image")
        self.assertEqual(font.glyph("B")["source"], "traced_image")
        self.assertGreaterEqual(len(font.glyph("A")["contours"]), 2)  # outer + inner counter hole!
        self.assertTrue(verify_truetype_bytes(font.to_ttf())["valid"])

    def test_blank_cell_abstention(self) -> None:
        blank_patch = [0.02] * 256
        res = synthesize_glyph_fast("Q", [4.0, 58.0, 0.70, 1.0, 0.55, 2.0, 0.15, 0.25], target_patch=blank_patch)
        self.assertTrue(res["is_missing"])
        self.assertGreater(res["p_missing"], 0.99)
        self.assertIsNone(res["value"])

    def test_indic_sanskrit_devanagari_and_multilingual(self) -> None:
        """TDD: Sanskrit/Devanagari and Indic scripts (Kannada, Tamil, Telugu, Bengali) synthesize biometric glyphs and compile valid .ttf."""
        sanskrit_font = scribefont(
            {"style": [6.0, 62.0, 0.72, 1.02, 0.65, 2.0, 0.2, 0.25]},
            family="ScribeSanskrit",
            script="sanskrit",
        )
        self.assertEqual(sanskrit_font.script, "sanskrit")
        self.assertTrue(sanskrit_font.invariants_passed)
        self.assertGreaterEqual(len(sanskrit_font.glyphs), len(DEVANAGARI_CHARSET))

        for ch in ("ॐ", "ऽ", "।", "॥", "क", "अ", "ऋ", "९"):
            g = sanskrit_font.glyph(ch)
            self.assertFalse(g["is_missing"])
            self.assertEqual(g["source"], "indic_biometric_bank")
            self.assertGreaterEqual(len(g["contours"]), 1)
            self.assertGreater(g["advance_width"], 150)

        for mark in ("े", "ै", "ु", "ू", "ृ", "्", "ं", "ँ"):
            gm = sanskrit_font.glyph(mark)
            self.assertTrue(gm["combining"])
            self.assertEqual(gm["advance_width"], 0)
            self.assertLess(gm["lsb"], 0)

        self.assertEqual(reorder_indic_visual_order("कि"), "िक")
        self.assertEqual(reorder_indic_visual_order("प्रि"), "िप्र")

        svg = sanskrit_font.render_svg("सत्यमेव जयते ॥ वसुधैव कुटुम्बकम् ॐ", size=52)
        self.assertIn("<svg", svg)
        self.assertIn("<path", svg)
        self.assertTrue(verify_truetype_bytes(sanskrit_font.to_ttf())["valid"])

        for script in ("kannada", "tamil", "telugu", "bengali", "multilingual"):
            f = scribefont(None, script=script, family=f"Scribe_{script}")
            self.assertTrue(f.invariants_passed)
            self.assertGreaterEqual(len(f.glyphs), len(INDIC_SCRIPTS[script]))
            self.assertTrue(verify_truetype_bytes(f.to_ttf())["valid"])


if __name__ == "__main__":
    unittest.main()
