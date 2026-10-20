import test, { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import scribefont, { verifyTrueTypeBytes, rasterizeStrokesToImage } from '../src/index.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');

function decodeImageViaPython(imgPath) {
  const py = '/Users/lika/labs/extract/.venv/bin/python';
  const script = `
import json, sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGBA')
w, h = im.size
print(json.dumps({'width': w, 'height': h, 'data': list(im.tobytes())}))
`;
  const stdout = execFileSync(py, ['-c', script, imgPath], { maxBuffer: 64 * 1024 * 1024 }).toString();
  const parsed = JSON.parse(stdout);
  return { width: parsed.width, height: parsed.height, data: new Uint8ClampedArray(parsed.data) };
}

describe('BDD Feature: Real Handwriting-to-Font from Internet Images & Web Canvas', () => {
  it('Scenario 1: Given a real internet handwriting specimen (Palmer Method 1901 from Wikimedia Commons), When converted via scribefont.fromImage, Then it extracts >=30 multi-contour glyphs and compiles a verified .ttf', () => {
    const imgPath = path.join(ROOT, 'docs/samples/internet/internet-palmer-1901.jpg');
    assert.ok(fs.existsSync(imgPath), 'Palmer 1901 internet image exists on disk');
    const imgData = decodeImageViaPython(imgPath);

    const font = scribefont.fromImage(imgData, { family: 'PalmerInternet1901' });
    assert.ok(font.traced_count >= 30, `Expected >= 30 traced glyphs, got ${font.traced_count}`);
    assert.equal(font.invariants_passed, true);

    const ttf = font.toTTF();
    const verification = verifyTrueTypeBytes(ttf);
    assert.equal(verification.valid, true);
    assert.equal(verification.checksum_ok, true);
  });

  it('Scenario 2: Given a real internet school handwritten alphabet sheet (Wikimedia Commons), When converted via scribefont.fromImage, Then it traces 60+ glyphs with outer & inner counter contours', () => {
    const imgPath = path.join(ROOT, 'docs/samples/internet/internet-school-alphabet.jpg');
    assert.ok(fs.existsSync(imgPath), 'School handwritten alphabet image exists on disk');
    const imgData = decodeImageViaPython(imgPath);

    const font = scribefont.fromImage(imgData, { family: 'SchoolHand' });
    assert.ok(font.traced_count >= 60, `Expected >= 60 traced glyphs, got ${font.traced_count}`);
    const svg = font.renderSVG('Handwriting from internet!');
    assert.ok(svg.includes('fill-rule="evenodd"'));
    assert.equal(verifyTrueTypeBytes(font.toTTF()).valid, true);
  });

  it('Scenario 3: Given a user writing freehand on the interactive Web Canvas pad, When converted via scribefont.fromCanvas, Then drawn characters are vector-traced with inner counter holes and unseen characters inherit measured biometrics', () => {
    // User draws 'A', 'B', 'O' on the web canvas
    const userCanvasStrokes = [
      // 'A'
      [[22, 82], [44, 18], [66, 82]],
      [[30, 56], [58, 56]],
      // 'B'
      [[96, 18], [96, 82]],
      [[96, 18], [126, 22], [126, 46], [96, 50], [128, 56], [128, 78], [96, 82]],
      // 'O'
      [[178, 18], [158, 32], [158, 68], [178, 82], [198, 68], [198, 32], [178, 18]],
    ];

    const font = scribefont.fromCanvas(userCanvasStrokes, {
      width: 240,
      height: 100,
      transcript: 'ABO',
      family: 'WebCanvasUserFont',
    });

    assert.equal(font.traced_count, 3);
    assert.equal(font.glyph('A').source, 'traced_image');
    assert.equal(font.glyph('B').source, 'traced_image');
    assert.equal(font.glyph('O').source, 'traced_image');
    // Verify multi-contour tracing captured inner counter holes!
    assert.ok(font.glyph('A').contours.length >= 2, 'Drawn A has outer boundary + inner counter hole');
    assert.ok(font.glyph('O').contours.length >= 2, 'Drawn O has outer boundary + inner counter hole');
    // Unseen character 'g' is synthesized from REAL_HANDWRITING_BANK using user's measured biometrics
    assert.equal(font.glyph('g').source, 'biometric_bank');
    assert.ok(font.glyph('g').contours.length >= 2);

    const ttf = font.toTTF();
    assert.equal(verifyTrueTypeBytes(ttf).valid, true);
  });
});
