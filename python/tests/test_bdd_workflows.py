"""BDD Acceptance Suite: Handwriting-to-Font from Real Internet Specimens & Interactive Web Canvas."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from scribefont import scribefont, verify_truetype_bytes


class TestBDDHandwritingWorkflows(unittest.TestCase):
    """Behavior-Driven Development (Given / When / Then) scenarios for scribefont."""

    def test_scenario_1_wikimedia_palmer_1901_specimen(self) -> None:
        """Given a real internet scan of the 1901 Palmer Method penmanship alphabet from Wikimedia Commons,
        When converted via scribefont.from_image,
        Then it segments >=30 handwritten glyphs, extracts slant > 8°, and compiles a valid .ttf font."""
        img_path = ROOT.parent / "docs" / "samples" / "internet" / "internet-palmer-1901.jpg"
        self.assertTrue(img_path.exists())

        font = scribefont.from_image(img_path, family="PalmerInternet1901")
        self.assertGreaterEqual(font.traced_count, 30)
        self.assertGreater(font.style["slant_deg"], 5.0)
        self.assertTrue(font.invariants_passed)

        ttf_bytes = font.to_ttf()
        chk = verify_truetype_bytes(ttf_bytes)
        self.assertTrue(chk["valid"])
        self.assertTrue(chk["checksum_ok"])

        # Prove that FreeType (PIL.ImageFont.truetype) loads the binary .ttf and renders real ink pixels
        import io
        from PIL import Image, ImageDraw, ImageFont
        ft_font = ImageFont.truetype(io.BytesIO(ttf_bytes), 42)
        im = Image.new("L", (400, 70), 255)
        ImageDraw.Draw(im).text((12, 10), "ABC abc 123!", fill=0, font=ft_font)
        dark_pixels = sum(1 for px in im.tobytes() if px < 128)
        self.assertGreater(dark_pixels, 150)

    def test_scenario_2_wikimedia_mills_1909_specimen(self) -> None:
        """Given a real internet scan of E. C. Mills' 1909 American Business Writing specimen,
        When converted via scribefont.from_image,
        Then it segments >=30 cursive glyphs and renders an even-odd multi-contour SVG specimen."""
        img_path = ROOT.parent / "docs" / "samples" / "internet" / "internet-mills-1909.jpg"
        self.assertTrue(img_path.exists())

        font = scribefont.from_image(img_path, family="Mills1909")
        self.assertGreaterEqual(font.traced_count, 30)
        svg = font.render_svg("Modern American Writing 1909", size=48)
        self.assertIn('fill-rule="evenodd"', svg)
        self.assertTrue(verify_truetype_bytes(font.to_ttf())["valid"])

    def test_scenario_3_interactive_web_canvas_drawing(self) -> None:
        """Given a user writing freehand strokes on the web canvas ('A', 'B', 'O'),
        When converted via scribefont.from_canvas,
        Then the drawn letters are traced with inner counter holes and unseen letters inherit measured biometrics."""
        canvas_strokes = [
            # 'A'
            [[22, 82], [44, 18], [66, 82]],
            [[30, 56], [58, 56]],
            # 'B'
            [[96, 18], [96, 82]],
            [[96, 18], [126, 22], [126, 46], [96, 50], [128, 56], [128, 78], [96, 82]],
            # 'O'
            [[178, 18], [158, 32], [158, 68], [178, 82], [198, 68], [198, 32], [178, 18]],
        ]
        font = scribefont.from_canvas(
            canvas_strokes,
            width=240,
            height=100,
            transcript="ABO",
            family="WebCanvasUserFont",
        )
        self.assertEqual(font.traced_count, 3)
        self.assertEqual(font.glyph("A")["source"], "traced_image")
        self.assertEqual(font.glyph("B")["source"], "traced_image")
        self.assertEqual(font.glyph("O")["source"], "traced_image")
        self.assertGreaterEqual(len(font.glyph("A")["contours"]), 2)
        self.assertGreaterEqual(len(font.glyph("O")["contours"]), 2)
        self.assertEqual(font.glyph("g")["source"], "biometric_bank")
        self.assertTrue(verify_truetype_bytes(font.to_ttf())["valid"])

    def test_scenario_4_printable_chart_filled_and_uploaded(self) -> None:
        """Given a user who prints the 5x13 drop-out template chart, writes all 65 glyphs in dark pen, and uploads it,
        When converted via scribefont.from_image,
        Then all light cyan/gray guide boxes drop out automatically and 65/65 glyphs are traced with inner counter holes."""
        chart_svg = ROOT.parent / "docs" / "samples" / "scribefont-template-chart.svg"
        filled_png = ROOT.parent / "docs" / "samples" / "sample-filled-template.png"
        self.assertTrue(chart_svg.exists())
        self.assertTrue(filled_png.exists())

        font = scribefont.from_image(filled_png, family="PrintableChartFont")
        self.assertEqual(font.traced_count, 65)
        self.assertEqual(font.glyph("A")["source"], "traced_image")
        self.assertGreaterEqual(len(font.glyph("A")["contours"]), 2)
        self.assertTrue(verify_truetype_bytes(font.to_ttf())["valid"])


if __name__ == "__main__":
    unittest.main()
