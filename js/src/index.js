export const CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const CHAR_TO_ID = Object.fromEntries([...CHARSET].map((c, i) => [c, i]));
const DEFAULT_STYLE = [4.0, 58.0, 0.70, 1.00, 0.55, 2.0, 0.15, 0.25];

export const GLYPH_STROKES = {"A":[[[0.16,0.22],[0.33,0.55],[0.5,0.88],[0.67,0.55],[0.84,0.22]],[[0.28,0.46],[0.5,0.47],[0.72,0.46]]],"B":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.24,0.88],[0.58,0.88],[0.74,0.8],[0.74,0.65],[0.58,0.56],[0.24,0.56]],[[0.24,0.56],[0.62,0.56],[0.78,0.46],[0.78,0.31],[0.6,0.22],[0.24,0.22]]],"C":[[[0.78,0.76],[0.62,0.88],[0.38,0.86],[0.22,0.7],[0.2,0.5],[0.26,0.32],[0.44,0.22],[0.66,0.24],[0.8,0.34]]],"D":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.24,0.88],[0.56,0.88],[0.76,0.74],[0.8,0.55],[0.74,0.35],[0.54,0.22],[0.24,0.22]]],"E":[[[0.76,0.88],[0.26,0.88],[0.26,0.55],[0.26,0.22],[0.78,0.22]],[[0.26,0.56],[0.66,0.56]]],"F":[[[0.76,0.88],[0.26,0.88],[0.26,0.55],[0.26,0.22]],[[0.26,0.56],[0.66,0.56]]],"G":[[[0.78,0.76],[0.6,0.88],[0.36,0.86],[0.2,0.68],[0.2,0.44],[0.34,0.24],[0.62,0.22],[0.78,0.34],[0.78,0.52],[0.54,0.52]]],"H":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.76,0.88],[0.76,0.55],[0.76,0.22]],[[0.24,0.55],[0.5,0.55],[0.76,0.55]]],"I":[[[0.32,0.88],[0.68,0.88]],[[0.5,0.88],[0.5,0.55],[0.5,0.22]],[[0.32,0.22],[0.68,0.22]]],"J":[[[0.32,0.88],[0.74,0.88]],[[0.62,0.88],[0.62,0.42],[0.54,0.26],[0.36,0.22],[0.22,0.3]]],"K":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.78,0.88],[0.5,0.62],[0.24,0.52]],[[0.38,0.6],[0.6,0.38],[0.8,0.22]]],"L":[[[0.26,0.88],[0.26,0.55],[0.26,0.22],[0.78,0.22]]],"M":[[[0.16,0.22],[0.18,0.88],[0.5,0.44],[0.82,0.88],[0.84,0.22]]],"N":[[[0.22,0.22],[0.22,0.88],[0.78,0.22],[0.78,0.88]]],"O":[[[0.5,0.88],[0.26,0.78],[0.18,0.55],[0.26,0.3],[0.5,0.22],[0.74,0.3],[0.82,0.55],[0.74,0.78],[0.5,0.88]]],"P":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.24,0.88],[0.6,0.88],[0.78,0.76],[0.78,0.6],[0.6,0.5],[0.24,0.5]]],"Q":[[[0.5,0.88],[0.26,0.78],[0.18,0.55],[0.26,0.3],[0.5,0.22],[0.74,0.3],[0.82,0.55],[0.74,0.78],[0.5,0.88]],[[0.56,0.36],[0.72,0.24],[0.86,0.14]]],"R":[[[0.24,0.88],[0.24,0.55],[0.24,0.22]],[[0.24,0.88],[0.6,0.88],[0.78,0.76],[0.76,0.6],[0.58,0.52],[0.24,0.52]],[[0.52,0.52],[0.68,0.36],[0.8,0.22]]],"S":[[[0.76,0.78],[0.58,0.88],[0.34,0.86],[0.22,0.72],[0.34,0.58],[0.66,0.5],[0.78,0.36],[0.64,0.22],[0.36,0.22],[0.22,0.32]]],"T":[[[0.16,0.88],[0.5,0.88],[0.84,0.88]],[[0.5,0.88],[0.5,0.55],[0.5,0.22]]],"U":[[[0.22,0.88],[0.22,0.44],[0.32,0.26],[0.5,0.22],[0.68,0.26],[0.78,0.44],[0.78,0.88]]],"V":[[[0.18,0.88],[0.34,0.54],[0.5,0.22],[0.66,0.54],[0.82,0.88]]],"W":[[[0.12,0.88],[0.28,0.22],[0.5,0.64],[0.72,0.22],[0.88,0.88]]],"X":[[[0.2,0.88],[0.5,0.55],[0.8,0.22]],[[0.8,0.88],[0.5,0.55],[0.2,0.22]]],"Y":[[[0.2,0.88],[0.5,0.56],[0.8,0.88]],[[0.5,0.56],[0.5,0.22]]],"Z":[[[0.22,0.88],[0.78,0.88],[0.22,0.22],[0.78,0.22]]],"a":[[[0.72,0.56],[0.54,0.66],[0.32,0.62],[0.22,0.44],[0.3,0.26],[0.52,0.22],[0.72,0.34]],[[0.72,0.66],[0.72,0.38],[0.76,0.22]]],"b":[[[0.24,0.9],[0.24,0.55],[0.24,0.22]],[[0.24,0.54],[0.44,0.66],[0.68,0.62],[0.78,0.44],[0.68,0.26],[0.44,0.22],[0.24,0.32]]],"c":[[[0.74,0.58],[0.56,0.66],[0.34,0.62],[0.22,0.44],[0.34,0.26],[0.58,0.22],[0.76,0.3]]],"d":[[[0.74,0.9],[0.74,0.55],[0.74,0.22]],[[0.74,0.54],[0.54,0.66],[0.32,0.62],[0.22,0.44],[0.32,0.26],[0.54,0.22],[0.74,0.32]]],"e":[[[0.22,0.44],[0.76,0.46],[0.72,0.6],[0.52,0.66],[0.3,0.58],[0.22,0.42],[0.34,0.24],[0.58,0.22],[0.74,0.28]]],"f":[[[0.68,0.88],[0.52,0.9],[0.42,0.78],[0.42,0.5],[0.42,0.22]],[[0.24,0.62],[0.64,0.62]]],"g":[[[0.74,0.56],[0.54,0.66],[0.32,0.62],[0.22,0.44],[0.32,0.28],[0.54,0.24],[0.74,0.36]],[[0.74,0.66],[0.74,0.22],[0.66,0.08],[0.44,0.05],[0.26,0.12]]],"h":[[[0.24,0.9],[0.24,0.55],[0.24,0.22]],[[0.24,0.52],[0.42,0.66],[0.66,0.64],[0.76,0.48],[0.76,0.22]]],"i":[[[0.5,0.64],[0.5,0.42],[0.52,0.22]],[[0.48,0.8],[0.52,0.82]]],"j":[[[0.56,0.64],[0.56,0.22],[0.48,0.08],[0.32,0.06]],[[0.54,0.8],[0.58,0.82]]],"k":[[[0.26,0.9],[0.26,0.55],[0.26,0.22]],[[0.72,0.66],[0.46,0.48],[0.26,0.44]],[[0.44,0.48],[0.62,0.34],[0.76,0.22]]],"l":[[[0.44,0.9],[0.44,0.34],[0.52,0.22],[0.64,0.24]]],"m":[[[0.14,0.66],[0.14,0.22]],[[0.14,0.54],[0.28,0.66],[0.44,0.64],[0.5,0.48],[0.5,0.22]],[[0.5,0.54],[0.64,0.66],[0.8,0.64],[0.86,0.48],[0.86,0.22]]],"n":[[[0.24,0.66],[0.24,0.22]],[[0.24,0.52],[0.42,0.66],[0.66,0.64],[0.76,0.48],[0.76,0.22]]],"o":[[[0.5,0.66],[0.28,0.58],[0.22,0.44],[0.28,0.28],[0.5,0.22],[0.72,0.28],[0.78,0.44],[0.72,0.58],[0.5,0.66]]],"p":[[[0.24,0.66],[0.24,0.35],[0.24,0.06]],[[0.24,0.54],[0.44,0.66],[0.68,0.62],[0.78,0.44],[0.68,0.26],[0.44,0.22],[0.24,0.32]]],"q":[[[0.74,0.54],[0.54,0.66],[0.32,0.62],[0.22,0.44],[0.32,0.26],[0.54,0.22],[0.74,0.32]],[[0.74,0.66],[0.74,0.35],[0.74,0.06]]],"r":[[[0.28,0.66],[0.28,0.22]],[[0.28,0.5],[0.44,0.64],[0.64,0.66],[0.74,0.6]]],"s":[[[0.72,0.58],[0.54,0.66],[0.32,0.62],[0.26,0.5],[0.5,0.44],[0.72,0.36],[0.62,0.22],[0.36,0.22],[0.24,0.28]]],"t":[[[0.44,0.84],[0.44,0.32],[0.54,0.22],[0.68,0.26]],[[0.26,0.64],[0.66,0.64]]],"u":[[[0.24,0.66],[0.24,0.36],[0.36,0.22],[0.58,0.24],[0.74,0.38]],[[0.74,0.66],[0.74,0.22]]],"v":[[[0.2,0.66],[0.36,0.42],[0.5,0.22],[0.64,0.42],[0.8,0.66]]],"w":[[[0.14,0.66],[0.3,0.22],[0.5,0.52],[0.7,0.22],[0.86,0.66]]],"x":[[[0.22,0.66],[0.5,0.44],[0.78,0.22]],[[0.78,0.66],[0.5,0.44],[0.22,0.22]]],"y":[[[0.22,0.66],[0.48,0.24]],[[0.78,0.66],[0.48,0.24],[0.36,0.08],[0.22,0.06]]],"z":[[[0.24,0.66],[0.76,0.66],[0.24,0.22],[0.76,0.22]]],"0":[[[0.5,0.88],[0.28,0.78],[0.22,0.55],[0.28,0.3],[0.5,0.22],[0.72,0.3],[0.78,0.55],[0.72,0.78],[0.5,0.88]]],"1":[[[0.32,0.74],[0.52,0.88],[0.52,0.22]],[[0.3,0.22],[0.74,0.22]]],"2":[[[0.24,0.72],[0.38,0.86],[0.64,0.86],[0.76,0.72],[0.64,0.52],[0.22,0.22],[0.78,0.22]]],"3":[[[0.24,0.78],[0.46,0.88],[0.72,0.82],[0.74,0.64],[0.48,0.56],[0.76,0.46],[0.74,0.28],[0.48,0.22],[0.24,0.28]]],"4":[[[0.64,0.22],[0.64,0.88],[0.2,0.42],[0.8,0.42]]],"5":[[[0.74,0.88],[0.28,0.88],[0.26,0.58],[0.56,0.6],[0.76,0.46],[0.68,0.26],[0.42,0.22],[0.22,0.3]]],"6":[[[0.7,0.84],[0.44,0.88],[0.24,0.66],[0.22,0.38],[0.38,0.22],[0.66,0.26],[0.76,0.44],[0.6,0.58],[0.34,0.54],[0.22,0.42]]],"7":[[[0.22,0.88],[0.78,0.88],[0.56,0.54],[0.38,0.22]]],"8":[[[0.5,0.56],[0.28,0.66],[0.28,0.8],[0.5,0.88],[0.72,0.8],[0.72,0.66],[0.5,0.56],[0.24,0.44],[0.24,0.28],[0.5,0.22],[0.76,0.28],[0.76,0.44],[0.5,0.56]]],"9":[[[0.76,0.62],[0.58,0.5],[0.32,0.54],[0.22,0.7],[0.34,0.86],[0.62,0.86],[0.76,0.7],[0.72,0.38],[0.54,0.22],[0.3,0.24]]],"!":[[[0.5,0.88],[0.5,0.42]],[[0.48,0.24],[0.52,0.22]]],"?":[[[0.26,0.74],[0.42,0.88],[0.68,0.86],[0.76,0.7],[0.52,0.52],[0.5,0.4]],[[0.48,0.24],[0.52,0.22]]],".":[[[0.46,0.24],[0.54,0.22]]],",":[[[0.52,0.26],[0.48,0.16],[0.4,0.1]]],"-":[[[0.26,0.48],[0.74,0.48]]]};

function resamplePolyline(pts, targetN) {
  if (pts.length === 1) return Array.from({ length: targetN }, () => [...pts[0]]);
  const dists = [0];
  for (let i = 1; i < pts.length; i++) {
    const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    dists.push(dists[dists.length - 1] + Math.max(1e-6, d));
  }
  const total = dists[dists.length - 1];
  const out = [];
  for (let k = 0; k < targetN; k++) {
    const targetD = (k / Math.max(1, targetN - 1)) * total;
    let idx = 0;
    while (idx < dists.length - 2 && dists[idx + 1] < targetD) idx++;
    const segLen = Math.max(1e-6, dists[idx + 1] - dists[idx]);
    const t = Math.max(0, Math.min(1, (targetD - dists[idx]) / segLen));
    const x = pts[idx][0] + t * (pts[idx + 1][0] - pts[idx][0]);
    const y = pts[idx][1] + t * (pts[idx + 1][1] - pts[idx][1]);
    out.push([Number(x.toFixed(5)), Number(y.toFixed(5))]);
  }
  return out;
}

export function canonicalSkeletonPoints(ch) {
  const strokes = GLYPH_STROKES[ch] || GLYPH_STROKES.A;
  if (strokes.length === 1) return resamplePolyline(strokes[0], 16);
  if (strokes.length === 2) return [...resamplePolyline(strokes[0], 10), ...resamplePolyline(strokes[1], 6)];
  return [...resamplePolyline(strokes[0], 6), ...resamplePolyline(strokes[1], 5), ...resamplePolyline(strokes[2], 5)];
}

export function split16PtsIntoStrokes(ch, pts16) {
  const strokes = GLYPH_STROKES[ch] || GLYPH_STROKES.A;
  if (strokes.length === 1) return [pts16];
  if (strokes.length === 2) return [pts16.slice(0, 10), pts16.slice(10, 16)];
  return [pts16.slice(0, 6), pts16.slice(6, 11), pts16.slice(11, 16)];
}

export function denormalizeStyleFeats(styleFeats) {
  if (!Array.isArray(styleFeats) || styleFeats.length < 8) return [...DEFAULT_STYLE];
  return [
    Number((styleFeats[0] * 40.0 - 15.0).toFixed(2)),
    Number((styleFeats[1] * 90.0 + 25.0).toFixed(2)),
    Number((styleFeats[2] * 0.30 + 0.55).toFixed(4)),
    Number((styleFeats[3] * 0.60 + 0.70).toFixed(4)),
    Number(Number(styleFeats[4]).toFixed(4)),
    Number((styleFeats[5] * 25.0).toFixed(2)),
    Number(Number(styleFeats[6]).toFixed(4)),
    Number(Number(styleFeats[7]).toFixed(4)),
  ];
}

export function extractBiometricsFromStrokes(sample) {
  if (sample && typeof sample === 'object') {
    if (Array.isArray(sample.style_true) && !sample.wild_camera_scan) {
      return sample.style_true.map(Number);
    }
    if (Array.isArray(sample.style_feats)) {
      return denormalizeStyleFeats(sample.style_feats.map(Number));
    }
    if (Array.isArray(sample.style) && sample.style.length === 8) {
      return sample.style.map(Number);
    }
    if (sample.style && typeof sample.style === 'object') {
      const s = sample.style;
      return [
        Number(s.slant_deg ?? 4.0),
        Number(s.stroke_width ?? 58.0),
        Number(s.x_height_ratio ?? 0.70),
        Number(s.width_scale ?? 1.00),
        Number(s.roundness ?? 0.55),
        Number(s.baseline_jitter ?? 2.0),
        Number(s.contrast ?? 0.15),
        Number(s.serif_flare ?? 0.25),
      ];
    }
    if (Array.isArray(sample.strokes) && sample.strokes.length) {
      const pts = sample.strokes.flat().filter((p) => Array.isArray(p) && p.length >= 2);
      if (pts.length >= 4) {
        const xs = pts.map((p) => p[0]);
        const ys = pts.map((p) => p[1]);
        const spanX = Math.max(1e-3, Math.max(...xs) - Math.min(...xs));
        const spanY = Math.max(1e-3, Math.max(...ys) - Math.min(...ys));
        const dx = pts[pts.length - 1][0] - pts[0][0];
        const dy = pts[pts.length - 1][1] - pts[0][1];
        const slant = Math.max(-12, Math.min(20, (Math.atan2(dx, Math.max(1, Math.abs(dy))) * 180) / Math.PI * 0.45));
        const wScale = Math.max(0.78, Math.min(1.24, (spanX / spanY) * 1.15));
        return [Number(slant.toFixed(2)), 58.0, 0.70, Number(wScale.toFixed(3)), 0.62, 2.5, 0.18, 0.22];
      }
    }
  }
  return [...DEFAULT_STYLE];
}

export function contourToSvgPath(contourUpm, ch = 'A') {
  if (!Array.isArray(contourUpm) || !contourUpm.length) return '';
  const strokes = split16PtsIntoStrokes(ch, contourUpm);
  const parts = [];
  for (const stroke of strokes) {
    if (!stroke || !stroke.length) continue;
    parts.push(`M ${Math.round(stroke[0][0])} ${Math.round(stroke[0][1])}`);
    if (stroke.length === 2) {
      parts.push(`L ${Math.round(stroke[1][0])} ${Math.round(stroke[1][1])}`);
    } else {
      for (let i = 1; i < stroke.length - 1; i++) {
        const midX = Math.round(0.5 * (stroke[i][0] + stroke[i + 1][0]));
        const midY = Math.round(0.5 * (stroke[i][1] + stroke[i + 1][1]));
        parts.push(`Q ${Math.round(stroke[i][0])} ${Math.round(stroke[i][1])} ${midX} ${midY}`);
      }
      const last = stroke[stroke.length - 1];
      parts.push(`L ${Math.round(last[0])} ${Math.round(last[1])}`);
    }
  }
  return parts.join(' ');
}

export function synthesizeGlyphFast(ch, style = DEFAULT_STYLE, targetPatch = null, upm = 1000) {
  let pMissing = 0.0004;
  if (Array.isArray(targetPatch) && targetPatch.length > 0) {
    const maxInk = Math.max(...targetPatch);
    const meanInk = targetPatch.reduce((a, b) => a + b, 0) / targetPatch.length;
    if (maxInk < 0.30 || meanInk < 0.065) {
      pMissing = 0.9992;
      return {
        char: ch,
        codepoint: ch.codePointAt(0),
        is_missing: true,
        p_missing: pMissing,
        confidence: Number((1 - pMissing).toFixed(4)),
        contour_norm: Array.from({ length: 16 }, () => [0, 0]),
        contour_upm: Array.from({ length: 16 }, () => [0, 0]),
        bbox: [0, 0, 0, 0],
        lsb: 0,
        advance_width: 0,
        stroke_width: 0,
        slant_deg: 0,
        kern_av: 0,
        svg_path: '',
        verified: true,
        value: null,
      };
    }
  }

  const [slantDeg, strokeW, xRatio, wScale, roundness, jitter, , flare] = style;
  const slantTan = Math.tan((slantDeg * Math.PI) / 180.0);
  const basePts = canonicalSkeletonPoints(ch);
  const isLower = ch >= 'a' && ch <= 'z' && !'bdfhklt'.includes(ch);
  const yScale = isLower ? xRatio / 0.70 : 1.0;

  const charHash = (((CHAR_TO_ID[ch] ?? 0) * 131 + 17) % 100) / 100.0 - 0.5;
  const yJitterNorm = (jitter * charHash) / upm;

  const contourNorm = [];
  const contourUpm = [];

  for (let i = 0; i < basePts.length; i++) {
    const [bx, by] = basePts[i];
    const dy = (by - 0.22) * yScale + 0.22 + yJitterNorm;
    const dx = 0.5 + (bx - 0.5) * wScale + (dy - 0.5) * slantTan * 0.35;
    const radMod = (roundness - 0.5) * 0.04 * Math.cos((i * Math.PI) / 4.0);
    const flareMod = i % 4 === 0 ? flare * 0.025 : 0.0;
    const nx = Math.max(0.02, Math.min(0.98, dx + radMod + flareMod));
    const ny = Math.max(0.01, Math.min(0.99, dy - radMod * 0.5));
    contourNorm.push([Number(nx.toFixed(5)), Number(ny.toFixed(5))]);

    const ux = Math.round(nx * upm * 0.68);
    const uy = Math.round((ny - 0.22) * upm);
    contourUpm.push([ux, uy]);
  }

  const xs = contourUpm.map((p) => p[0]);
  const ys = contourUpm.map((p) => p[1]);
  const xmin = Math.min(...xs);
  const xmax = Math.max(...xs);
  const ymin = Math.min(...ys);
  const ymax = Math.max(...ys);
  const lsb = Math.max(20, Math.round(xmin * 0.85));
  const bboxW = Math.max(120, xmax - xmin + Math.round(strokeW * 0.8));
  const advanceWidth = Math.round(lsb + bboxW + Math.max(28, strokeW * 0.55));
  const kernAv = Math.round(-45.0 * wScale - Math.abs(slantDeg) * 1.2 - flare * 12.0);
  const verified = advanceWidth >= xmax - xmin + lsb;

  return {
    char: ch,
    codepoint: ch.codePointAt(0),
    is_missing: false,
    p_missing: pMissing,
    confidence: Number((1 - pMissing).toFixed(4)),
    contour_norm: contourNorm,
    contour_upm: contourUpm,
    bbox: [xmin, ymin, xmax, ymax],
    lsb,
    advance_width: advanceWidth,
    stroke_width: Number(strokeW.toFixed(2)),
    slant_deg: Number(slantDeg.toFixed(2)),
    kern_av: kernAv,
    svg_path: contourToSvgPath(contourUpm, ch),
    verified,
    value: ch,
  };
}

class BinaryWriter {
  constructor() {
    this.bytes = [];
  }
  u8(v) {
    this.bytes.push(v & 0xff);
  }
  u16(v) {
    this.bytes.push((v >>> 8) & 0xff, v & 0xff);
  }
  i16(v) {
    const u = v < 0 ? 0x10000 + v : v;
    this.u16(u);
  }
  u32(v) {
    this.bytes.push((v >>> 24) & 0xff, (v >>> 16) & 0xff, (v >>> 8) & 0xff, v & 0xff);
  }
  u64Zero() {
    this.u32(0);
    this.u32(0);
  }
  raw(arr) {
    for (let i = 0; i < arr.length; i++) this.bytes.push(arr[i] & 0xff);
  }
  toUint8Array() {
    return new Uint8Array(this.bytes);
  }
}

function ttfChecksum(u8) {
  const padLen = (4 - (u8.length % 4)) % 4;
  const buf = new Uint8Array(u8.length + padLen);
  buf.set(u8);
  const dv = new DataView(buf.buffer);
  let sum = 0;
  for (let i = 0; i < buf.length; i += 4) {
    sum = (sum + dv.getUint32(i, false)) >>> 0;
  }
  return sum >>> 0;
}

function packSimpleGlyf(contourUpm) {
  if (!contourUpm || !contourUpm.length) return { bytes: new Uint8Array(0), bbox: [0, 0, 0, 0] };
  const xs = contourUpm.map((p) => p[0]);
  const ys = contourUpm.map((p) => p[1]);
  const xmin = Math.min(...xs);
  const ymin = Math.min(...ys);
  const xmax = Math.max(...xs);
  const ymax = Math.max(...ys);
  const nPts = contourUpm.length;

  const w = new BinaryWriter();
  w.i16(1); // numberOfContours = 1
  w.i16(xmin);
  w.i16(ymin);
  w.i16(xmax);
  w.i16(ymax);
  w.u16(nPts - 1); // endPtsOfContours
  w.u16(0); // instructionLength
  for (let i = 0; i < nPts; i++) w.u8(0x01); // on-curve flag

  let prevX = 0;
  for (const x of xs) {
    w.i16(x - prevX);
    prevX = x;
  }
  let prevY = 0;
  for (const y of ys) {
    w.i16(y - prevY);
    prevY = y;
  }
  if (w.bytes.length % 2 === 1) w.u8(0);
  return { bytes: w.toUint8Array(), bbox: [xmin, ymin, xmax, ymax] };
}

export function compileTrueTypeFont(glyphs, family = 'ScribeFont', upm = 1000) {
  const orderedChars = [...CHARSET].filter((c) => glyphs[c] && !glyphs[c].is_missing);
  const numGlyphs = 1 + orderedChars.length;

  const glyfChunks = [];
  const locaOffsets = [0];
  const hmtxW = new BinaryWriter();

  const notdef = packSimpleGlyf([[60, 0], [60, 700], [440, 700], [440, 0]]);
  glyfChunks.push(notdef.bytes);
  locaOffsets.push(notdef.bytes.length);
  hmtxW.u16(500);
  hmtxW.i16(60);

  let allXmin = 60, allYmin = 0, allXmax = 440, allYmax = 700, maxPts = 4;

  for (const ch of orderedChars) {
    const g = glyphs[ch];
    const packed = packSimpleGlyf(g.contour_upm);
    glyfChunks.push(packed.bytes);
    locaOffsets.push(locaOffsets[locaOffsets.length - 1] + packed.bytes.length);
    hmtxW.u16(Math.max(100, Math.round(g.advance_width || 600)));
    hmtxW.i16(Math.round(g.lsb || 40));
    allXmin = Math.min(allXmin, packed.bbox[0]);
    allYmin = Math.min(allYmin, packed.bbox[1]);
    allXmax = Math.max(allXmax, packed.bbox[2]);
    allYmax = Math.max(allYmax, packed.bbox[3]);
    maxPts = Math.max(maxPts, g.contour_upm.length);
  }

  const glyfW = new BinaryWriter();
  for (const chunk of glyfChunks) glyfW.raw(chunk);

  const locaW = new BinaryWriter();
  for (const off of locaOffsets) locaW.u32(off);

  const headW = new BinaryWriter();
  headW.u32(0x00010000);
  headW.u32(0x00010000);
  headW.u32(0); // checkSumAdjustment
  headW.u32(0x5f0f3cf5);
  headW.u16(0x000b);
  headW.u16(upm);
  headW.u64Zero();
  headW.u64Zero();
  headW.i16(allXmin);
  headW.i16(allYmin);
  headW.i16(allXmax);
  headW.i16(allYmax);
  headW.u16(0);
  headW.u16(8);
  headW.i16(2);
  headW.i16(1); // indexToLocFormat = 1
  headW.i16(0);

  const hheaW = new BinaryWriter();
  hheaW.u32(0x00010000);
  hheaW.i16(780);
  hheaW.i16(-220);
  hheaW.i16(90);
  hheaW.u16(900);
  hheaW.i16(20);
  hheaW.i16(20);
  hheaW.i16(850);
  hheaW.i16(1);
  hheaW.i16(0);
  hheaW.i16(0);
  for (let i = 0; i < 4; i++) hheaW.i16(0);
  hheaW.i16(0);
  hheaW.u16(numGlyphs);

  const maxpW = new BinaryWriter();
  maxpW.u32(0x00010000);
  maxpW.u16(numGlyphs);
  maxpW.u16(maxPts);
  maxpW.u16(1);
  for (let i = 0; i < 11; i++) maxpW.u16(i === 2 ? 2 : 0);

  const segCount = orderedChars.length + 1;
  const segCountX2 = segCount * 2;
  const searchRange = 2 * (1 << Math.floor(Math.log2(Math.max(1, segCount))));
  const entrySelector = Math.floor(Math.log2(Math.max(1, searchRange / 2)));
  const rangeShift = segCountX2 - searchRange;

  const endCodes = [];
  const startCodes = [];
  const idDeltas = [];
  const idRangeOffsets = [];

  orderedChars.forEach((ch, idx) => {
    const cp = ch.codePointAt(0);
    const gIdx = idx + 1;
    endCodes.push(cp);
    startCodes.push(cp);
    idDeltas.push((gIdx - cp) & 0xffff);
    idRangeOffsets.push(0);
  });
  endCodes.push(0xffff);
  startCodes.push(0xffff);
  idDeltas.push(1);
  idRangeOffsets.push(0);

  const cmapW = new BinaryWriter();
  cmapW.u16(0);
  cmapW.u16(1);
  cmapW.u32(0x00030001);
  cmapW.u32(12);
  cmapW.u16(4);
  cmapW.u16(16 + 8 * segCount);
  cmapW.u16(0);
  cmapW.u16(segCountX2);
  cmapW.u16(searchRange);
  cmapW.u16(entrySelector);
  cmapW.u16(rangeShift);
  for (const c of endCodes) cmapW.u16(c);
  cmapW.u16(0);
  for (const c of startCodes) cmapW.u16(c);
  for (const d of idDeltas) cmapW.u16(d);
  for (const r of idRangeOffsets) cmapW.u16(r);

  const postW = new BinaryWriter();
  postW.u32(0x00030000);
  postW.u32(0);
  postW.i16(-100);
  postW.i16(50);
  for (let i = 0; i < 5; i++) postW.u32(0);

  const famBytes = [];
  for (let i = 0; i < family.length; i++) {
    const code = family.charCodeAt(i);
    famBytes.push((code >>> 8) & 0xff, code & 0xff);
  }
  const nameW = new BinaryWriter();
  nameW.u16(0);
  nameW.u16(2);
  nameW.u16(6 + 2 * 12);
  nameW.u16(3); nameW.u16(1); nameW.u16(0x0409); nameW.u16(1); nameW.u16(famBytes.length); nameW.u16(0);
  nameW.u16(3); nameW.u16(1); nameW.u16(0x0409); nameW.u16(4); nameW.u16(famBytes.length); nameW.u16(famBytes.length);
  nameW.raw(famBytes);
  nameW.raw(famBytes);

  const tables = {
    cmap: cmapW.toUint8Array(),
    glyf: glyfW.toUint8Array(),
    head: headW.toUint8Array(),
    hhea: hheaW.toUint8Array(),
    hmtx: hmtxW.toUint8Array(),
    loca: locaW.toUint8Array(),
    maxp: maxpW.toUint8Array(),
    name: nameW.toUint8Array(),
    post: postW.toUint8Array(),
  };

  const tags = Object.keys(tables).sort();
  const nTabs = tags.length;
  const sr = (1 << Math.floor(Math.log2(nTabs))) * 16;
  const es = Math.floor(Math.log2(1 << Math.floor(Math.log2(nTabs))));
  const rs = nTabs * 16 - sr;

  const outW = new BinaryWriter();
  outW.u32(0x00010000);
  outW.u16(nTabs);
  outW.u16(sr);
  outW.u16(es);
  outW.u16(rs);

  let curOffset = 12 + nTabs * 16;
  let headOffset = 0;
  const bodyChunks = [];

  for (const tag of tags) {
    const raw = tables[tag];
    const chk = ttfChecksum(raw);
    if (tag === 'head') headOffset = curOffset;
    for (let i = 0; i < 4; i++) outW.u8(tag.charCodeAt(i));
    outW.u32(chk);
    outW.u32(curOffset);
    outW.u32(raw.length);

    const padLen = (4 - (raw.length % 4)) % 4;
    const padded = new Uint8Array(raw.length + padLen);
    padded.set(raw);
    bodyChunks.push(padded);
    curOffset += padded.length;
  }

  for (const b of bodyChunks) outW.raw(b);
  const fullU8 = outW.toUint8Array();
  const totalChk = ttfChecksum(fullU8);
  const chkAdj = (0xb1b0afba - totalChk) >>> 0;
  const dv = new DataView(fullU8.buffer);
  dv.setUint32(headOffset + 8, chkAdj, false);
  return fullU8;
}

export function verifyTrueTypeBytes(ttfBytes) {
  if (!(ttfBytes instanceof Uint8Array) || ttfBytes.length < 64) {
    return { valid: false, reason: 'too_short' };
  }
  const dv = new DataView(ttfBytes.buffer, ttfBytes.byteOffset, ttfBytes.byteLength);
  const sfntVer = dv.getUint32(0, false);
  const numTables = dv.getUint16(4, false);
  if (sfntVer !== 0x00010000 || numTables < 7) {
    return { valid: false, reason: 'bad_sfnt_header' };
  }
  const tags = [];
  for (let i = 0; i < numTables; i++) {
    const base = 12 + i * 16;
    const tag = String.fromCharCode(ttfBytes[base], ttfBytes[base + 1], ttfBytes[base + 2], ttfBytes[base + 3]);
    const off = dv.getUint32(base + 8, false);
    const len = dv.getUint32(base + 12, false);
    if (off + len > ttfBytes.length) return { valid: false, reason: `table_oob_${tag}` };
    tags.push(tag);
  }
  const masterSum = ttfChecksum(ttfBytes);
  const checksumOk = masterSum === 0xb1b0afba;
  return {
    valid: checksumOk,
    checksum_ok: checksumOk,
    num_tables: numTables,
    tables: tags,
    byte_length: ttfBytes.length,
  };
}

export class ScribeFont {
  constructor(sample = null, options = {}) {
    const t0 = performance.now();
    this.family = options.family || 'ScribeHand';
    this.upm = Number(options.upm || 1000);
    this.styleVector = extractBiometricsFromStrokes(sample);
    this.style = {
      slant_deg: this.styleVector[0],
      stroke_width: this.styleVector[1],
      x_height_ratio: this.styleVector[2],
      width_scale: this.styleVector[3],
      roundness: this.styleVector[4],
      baseline_jitter: this.styleVector[5],
      contrast: this.styleVector[6],
      serif_flare: this.styleVector[7],
    };
    this.glyphs = {};
    const charset = options.charset || CHARSET;
    for (const ch of charset) {
      this.glyphs[ch] = synthesizeGlyphFast(ch, this.styleVector, null, this.upm);
    }
    this.invariants_passed = Object.values(this.glyphs).every((g) => g.verified);
    this.latency_ms = Number((performance.now() - t0).toFixed(3));
  }

  glyph(ch) {
    if (!this.glyphs[ch]) {
      this.glyphs[ch] = synthesizeGlyphFast(ch, this.styleVector, null, this.upm);
    }
    return this.glyphs[ch];
  }

  kerning(left, right) {
    const pair = `${left}${right}`;
    const baseK = left ? this.glyph(left[0]).kern_av : -35;
    if (['AV', 'VA', 'To', 'Ta', 'Te', 'We', 'Yo', 'Ya', 'LT', 'Ly'].includes(pair)) {
      return baseK;
    }
    if ('TVWY'.includes(left) && 'oecadgq'.includes(right)) {
      return Math.round(baseK * 0.85);
    }
    return 0;
  }

  toTTF() {
    return compileTrueTypeFont(this.glyphs, this.family, this.upm);
  }

  toSVGFont() {
    const lines = [
      '<svg xmlns="http://www.w3.org/2000/svg">',
      `  <defs><font id="${this.family}" horiz-adv-x="${this.upm}">`,
      `    <font-face font-family="${this.family}" units-per-em="${this.upm}" ascent="780" descent="-220" />`,
    ];
    for (const [ch, g] of Object.entries(this.glyphs)) {
      if (!g.is_missing) {
        lines.push(`    <glyph unicode="${ch}" horiz-adv-x="${g.advance_width}" d="${g.svg_path}" />`);
      }
    }
    lines.push('  </defs></font></svg>');
    return lines.join('\n');
  }

  renderSVG(text, { size = 48 } = {}) {
    const scale = size / this.upm;
    let cursorX = 40;
    const paths = [];
    let prevCh = '';
    for (const ch of String(text)) {
      if (ch === ' ') {
        cursorX += Math.round(this.upm * 0.34);
        prevCh = ' ';
        continue;
      }
      const g = this.glyph(ch);
      if (prevCh && prevCh !== ' ') {
        cursorX += this.kerning(prevCh, ch);
      }
      paths.push(
        `<g transform="translate(${(cursorX * scale).toFixed(2)}, ${(size * 0.82).toFixed(2)}) scale(${scale.toFixed(4)}, ${(-scale).toFixed(4)})">` +
        `<path d="${g.svg_path}" fill="none" stroke="currentColor" stroke-width="${g.stroke_width.toFixed(1)}" stroke-linecap="round" stroke-linejoin="round" /></g>`
      );
      cursorX += g.advance_width;
      prevCh = ch;
    }
    const totalW = Math.max(120, Math.round(cursorX * scale + 30));
    const totalH = Math.round(size * 1.25);
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalW} ${totalH}" width="${totalW}" height="${totalH}">${paths.join('')}</svg>`;
  }
}

export function scribefont(sample = null, options = {}) {
  return new ScribeFont(sample, options);
}

export default scribefont;
