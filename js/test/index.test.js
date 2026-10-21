import test from 'node:test';
import assert from 'node:assert/strict';
import scribefont, {
  verifyTrueTypeBytes,
  synthesizeGlyphFast,
  reorderIndicVisualOrder,
  DEVANAGARI_CHARSET,
  INDIC_SCRIPTS,
} from '../src/index.js';

test('scribefont synthesizes 62 multi-contour handwritten glyphs, optical kerning, SVG, and valid binary .ttf', () => {
  const font = scribefont(
    {
      style: {
        slant_deg: 14.5,
        stroke_width: 52,
        x_height_ratio: 0.68,
        width_scale: 0.95,
        roundness: 0.78,
        baseline_jitter: 3.0,
        contrast: 0.45,
        serif_flare: 0.50,
      },
    },
    { family: 'MiraScript' }
  );

  assert.equal(font.family, 'MiraScript');
  assert.equal(font.invariants_passed, true);
  assert.ok(Object.keys(font.glyphs).length >= 62);

  const gA = font.glyph('A');
  assert.equal(gA.char, 'A');
  assert.equal(gA.is_missing, false);
  assert.ok(gA.p_missing < 0.01);
  assert.ok(gA.contours.length >= 2); // outer contour + inner counter hole
  assert.equal(gA.contour_upm.length, 16);
  assert.ok(gA.svg_path.startsWith('M '));

  const kernAV = font.kerning('A', 'V');
  assert.ok(kernAV < -20);

  const svg = font.renderSVG('Hello Scribe 2026', { size: 48 });
  assert.ok(svg.includes('<svg'));
  assert.ok(svg.includes('<path'));

  const ttf = font.toTTF();
  const check = verifyTrueTypeBytes(ttf);
  assert.equal(check.valid, true);
  assert.equal(check.checksum_ok, true);
  assert.ok(check.byte_length > 8000);
});

test('scribefont.fromImage traces synthetic handwriting image bitmap into valid multi-contour .ttf', () => {
  const W = 120, H = 60;
  const data = new Uint8ClampedArray(W * H * 4).fill(250);
  // Draw two dark handwritten strokes ('I' and 'O')
  for (let r = 12; r < 48; r++) {
    for (let c = 18; c < 25; c++) {
      const idx = (r * W + c) * 4;
      data[idx] = 20; data[idx + 1] = 20; data[idx + 2] = 25;
    }
  }
  for (let r = 14; r < 46; r++) {
    for (let c = 50; c < 82; c++) {
      const dist = Math.hypot(c - 66, r - 30);
      if (dist >= 9 && dist <= 15) {
        const idx = (r * W + c) * 4;
        data[idx] = 20; data[idx + 1] = 20; data[idx + 2] = 25;
      }
    }
  }
  const font = scribefont.fromImage({ width: W, height: H, data }, { transcript: 'IO', family: 'ScanHand' });
  assert.equal(font.traced_count, 2);
  assert.equal(font.glyph('I').source, 'traced_image');
  assert.equal(font.glyph('O').source, 'traced_image');
  assert.ok(font.glyph('O').contours.length >= 2); // outer + inner hole traced!
  const ttf = font.toTTF();
  assert.equal(verifyTrueTypeBytes(ttf).valid, true);
});

test('scribefont.fromCanvas rasterizes and traces freehand web canvas strokes into multi-contour .ttf', () => {
  assert.equal(typeof scribefont.fromCanvas, 'function');
  const strokes = [
    [[24, 78], [44, 18], [64, 78]],
    [[31, 54], [57, 54]],
    [[95, 18], [95, 78]],
    [[95, 18], [122, 22], [122, 45], [95, 48], [125, 54], [125, 75], [95, 78]],
  ];
  const font = scribefont.fromCanvas(strokes, { width: 220, height: 96, transcript: 'AB', family: 'CanvasHand' });
  assert.ok(font.traced_count >= 2);
  assert.equal(font.glyph('A').source, 'traced_image');
  assert.equal(font.glyph('B').source, 'traced_image');
  assert.ok(font.glyph('A').contours.length >= 2);
  assert.equal(verifyTrueTypeBytes(font.toTTF()).valid, true);
});

test('synthesizeGlyphFast abstains with calibrated p_missing on blank/smudge cells', () => {
  const blankPatch = Array(256).fill(0.02);
  const res = synthesizeGlyphFast('Q', undefined, blankPatch);
  assert.equal(res.is_missing, true);
  assert.ok(res.p_missing > 0.99);
  assert.equal(res.value, null);
});

test('scribefont supports Sanskrit, Devanagari, Kannada, Tamil, Telugu, and Bengali handwritten glyphs and .ttf export', () => {
  const sanskritFont = scribefont({ style: [6.0, 62.0, 0.72, 1.02, 0.65, 2.0, 0.2, 0.25] }, {
    family: 'ScribeSanskrit',
    script: 'sanskrit',
  });
  assert.equal(sanskritFont.script, 'sanskrit');
  assert.equal(sanskritFont.invariants_passed, true);
  assert.ok(Object.keys(sanskritFont.glyphs).length >= DEVANAGARI_CHARSET.length);

  // Verify Sanskrit Om (ॐ), Avagraha (ऽ), Danda (।), Double Danda (॥), and Ka (क)
  for (const ch of ['ॐ', 'ऽ', '।', '॥', 'क', 'अ', 'ऋ', '९']) {
    const g = sanskritFont.glyph(ch);
    assert.equal(g.is_missing, false);
    assert.equal(g.source, 'indic_biometric_bank');
    assert.ok(g.contours.length >= 1);
    assert.ok(g.advance_width > 150);
  }

  // Verify zero-advance combining vowel marks & virama
  for (const mark of ['े', 'ै', 'ु', 'ू', 'ृ', '्', 'ं', 'ँ']) {
    const gm = sanskritFont.glyph(mark);
    assert.equal(gm.combining, true);
    assert.equal(gm.advance_width, 0);
    assert.ok(gm.lsb < 0);
  }

  // Verify pre-base short-i matra ('ि') logical-to-visual reordering
  assert.equal(reorderIndicVisualOrder('कि'), 'िक');
  assert.equal(reorderIndicVisualOrder('प्रि'), 'िप्र');

  const svg = sanskritFont.renderSVG('सत्यमेव जयते ॥ वसुधैव कुटुम्बकम् ॐ', { size: 52 });
  assert.ok(svg.includes('<svg'));
  assert.ok(svg.includes('<path'));

  const ttf = sanskritFont.toTTF();
  const check = verifyTrueTypeBytes(ttf);
  assert.equal(check.valid, true);
  assert.equal(check.checksum_ok, true);

  // Verify Kannada, Tamil, Telugu, and Bengali scripts compile valid .ttf fonts
  for (const script of ['kannada', 'tamil', 'telugu', 'bengali', 'multilingual']) {
    const f = scribefont(null, { script, family: `Scribe_${script}` });
    assert.equal(f.invariants_passed, true);
    assert.ok(Object.keys(f.glyphs).length >= INDIC_SCRIPTS[script].length);
    assert.equal(verifyTrueTypeBytes(f.toTTF()).valid, true);
  }
});
