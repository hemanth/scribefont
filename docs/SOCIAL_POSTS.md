# ScribeFont Social Posts (X / Twitter & LinkedIn)

- **GIF to attach**: `/Users/lika/labs/scribefont/docs/scribefont-social.gif`
- **Best time to post (PT)**:
  - **X / Twitter**: Wednesday **6:00 AM - 8:30 AM PT** (put links in Reply #1)
  - **LinkedIn**: Wednesday **7:30 AM - 9:00 AM PT**

---

## X / Twitter

### Main Tweet (attach `scribefont-social.gif`)

```text
Even though my handwriting isn't great, I always wanted to create fonts from it.

Every tool I tried made me print a 100-box template or wrestle with FontForge.

So I built scribefont. Upload a photo of your handwriting (or draw a few strokes) and it compiles a 7KB .ttf font in 0.03ms:

const ttf = scribefont({ strokes }).toTTF();

That's it. Zero dependencies. Works in JS, Python, and the browser.
```

### Reply #1 (Links)

```text
Upload a handwriting photo or sketch a few letters in the browser:
https://hemanth.github.io/scribefont/

GitHub + 3.1MB Browser WASM ONNX model:
https://github.com/hemanth/scribefont
https://www.npmjs.com/package/scribefont

npm i scribefont
pip install scribefont
```

---

## LinkedIn (attach `scribefont-social.gif`)

```text
Even though my handwriting isn't great, I always wanted to create fonts from it.

Every time I tried, the process was painful. You had to print out a 100-box template sheet, scan every single letter, upload it to a paid web service, or compile C++ font toolchains just to get a working .ttf file.

Why should turning your handwriting into a font require all that?

So I built scribefont.

You can upload a photo of your handwriting (notebook page, whiteboard, or iPad sketch) or draw a few strokes right on the canvas. It extracts how your hand moves: slant, stroke weight, roundness, and x-height. From there, it generates quadratic Bezier curves for all 62 alphanumeric glyphs and packs the 9 OpenType binary tables directly in memory.

import scribefont from 'scribefont';

const font = scribefont({ strokes });
const ttf = font.toTTF(); // 7,292-byte installable .ttf

That's it. No FontForge. No native bindings. Just `npm i scribefont` or `pip install scribefont`.

It ships with a 3.1MB quantized ONNX model that runs right in the browser over WebAssembly SIMD in under 1ms, plus a zero-dependency JS and Python engine that compiles your font in 0.031ms.

Upload a photo of your handwriting (or scribble a few letters) in the browser studio and download your .ttf:
https://hemanth.github.io/scribefont/

Repo: https://github.com/hemanth/scribefont
npm: https://www.npmjs.com/package/scribefont

Let me know if you'd use it!

#javascript #python #opensource #webassembly #typography
```
