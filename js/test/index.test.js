import test from 'node:test';
import assert from 'node:assert/strict';
import scribefont, { verifyTrueTypeBytes, synthesizeGlyphFast } from '../src/index.js';

test('scribefont synthesizes 62 glyphs, optical kerning, SVG, and valid binary .ttf', () => {
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
  assert.equal(Object.keys(font.glyphs).length, 62);

  const gA = font.glyph('A');
  assert.equal(gA.char, 'A');
  assert.equal(gA.is_missing, false);
  assert.ok(gA.p_missing < 0.01);
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
  assert.ok(check.byte_length > 2000);
});

test('synthesizeGlyphFast abstains with calibrated p_missing on blank/smudge cells', () => {
  const blankPatch = Array(256).fill(0.02);
  const res = synthesizeGlyphFast('Q', undefined, blankPatch);
  assert.equal(res.is_missing, true);
  assert.ok(res.p_missing > 0.99);
  assert.equal(res.value, null);
});
