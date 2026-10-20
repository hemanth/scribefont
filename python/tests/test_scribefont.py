"""Unit tests for scribefont Python engine, Image-to-Font vectorizer, and binary TrueType (.ttf) compiler."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from scribefont import scribefont, synthesize_glyph_fast, verify_truetype_bytes


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
        self.assertEqual(len(font.glyphs), 62)

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

    def test_blank_cell_abstention(self) -> None:
        blank_patch = [0.02] * 256
        res = synthesize_glyph_fast("Q", [4.0, 58.0, 0.70, 1.0, 0.55, 2.0, 0.15, 0.25], target_patch=blank_patch)
        self.assertTrue(res["is_missing"])
        self.assertGreater(res["p_missing"], 0.99)
        self.assertIsNone(res["value"])


if __name__ == "__main__":
    unittest.main()
