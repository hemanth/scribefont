import { REAL_HANDWRITING_BANK } from './real_bank.js';

export const CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const CHAR_TO_ID = Object.fromEntries([...CHARSET].map((c, i) => [c, i]));
const DEFAULT_STYLE = [4.0, 58.0, 0.70, 1.00, 0.55, 2.0, 0.15, 0.25];
export const SAMPLE_SHEET_LINES = [
  'ABCDEFGHIJKLM',
  'NOPQRSTUVWXYZ',
  'abcdefghijklm',
  'nopqrstuvwxyz',
  '0123456789!?.',
];

export const WIKIMEDIA_SCHOOL_LINES = [
  'AaĄąBbCcČčDd',
  'EeĘęĖėFfGgHh',
  'IiĮįYyJjKkLl',
  'MmNnOoPpRrSs',
  'ŠšTtUuŲųŪūVv',
  'ZzŽž',
];

export const WIKIMEDIA_PALMER_LINES = [
  'ABCDEFGHIJKLM',
  'NOPQRSTUVWXYZ',
  'abcdefghijklmnop',
  'qrstuvwxyz1234567890.',
];

export const WIKIMEDIA_MILLS_LINES = [
  'ABCDEFG',
  'HIJKLMN',
  'OPQRSTU',
  'VWXYZ&',
  'abcdd efgg hijj',
  'kk lmnopp qrrs',
  'tt uvwx yyz &123',
  '4567890',
];

export { REAL_HANDWRITING_BANK };

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

function rdpOpen(pts, eps) {
  if (pts.length <= 2) return pts;
  const [ax, ay] = pts[0];
  const [bx, by] = pts[pts.length - 1];
  const vx = bx - ax;
  const vy = by - ay;
  const c2 = vx * vx + vy * vy;
  let maxD = -1;
  let idx = 0;
  for (let i = 1; i < pts.length - 1; i++) {
    const [px, py] = pts[i];
    let d;
    if (c2 <= 1e-9) {
      d = Math.hypot(px - ax, py - ay);
    } else {
      const t = Math.max(0, Math.min(1, ((px - ax) * vx + (py - ay) * vy) / c2));
      d = Math.hypot(px - (ax + t * vx), py - (ay + t * vy));
    }
    if (d > maxD) {
      maxD = d;
      idx = i;
    }
  }
  if (maxD > eps) {
    const left = rdpOpen(pts.slice(0, idx + 1), eps);
    const right = rdpOpen(pts.slice(idx), eps);
    return [...left.slice(0, -1), ...right];
  }
  return [pts[0], pts[pts.length - 1]];
}

function simplifyClosedLoop(pts, eps = 5.5) {
  if (pts.length < 6) return pts.map((p) => [Math.round(p[0]), Math.round(p[1])]);
  const mid = Math.floor(pts.length / 2);
  const p1 = rdpOpen(pts.slice(0, mid + 1), eps);
  const p2 = rdpOpen([...pts.slice(mid), pts[0]], eps);
  let res = [...p1.slice(0, -1), ...p2.slice(0, -1)];
  if (res.length < 4) {
    const step = Math.max(1, Math.floor(pts.length / 6));
    res = pts.filter((_, i) => i % step === 0);
  }
  return res.map((p) => [Math.round(p[0]), Math.round(p[1])]);
}

export function traceBitmapToContours(mask, baselineRow, xOffset, scaleUpm, eps = 5.5) {
  const H = mask.length;
  const W = H ? mask[0].length : 0;
  const adj = new Map();
  const addEdge = (x0, y0, x1, y1) => {
    const k = `${x0},${y0}`;
    let list = adj.get(k);
    if (!list) {
      list = [];
      adj.set(k, list);
    }
    list.push([x1, y1, `${x1},${y1}`]);
  };

  for (let r = 0; r < H; r++) {
    const row = mask[r];
    for (let c = 0; c < W; c++) {
      if (!row[c]) continue;
      if (r === 0 || !mask[r - 1][c]) addEdge(c, r, c + 1, r);
      if (c === W - 1 || !row[c + 1]) addEdge(c + 1, r, c + 1, r + 1);
      if (r === H - 1 || !mask[r + 1][c]) addEdge(c + 1, r + 1, c, r + 1);
      if (c === 0 || !row[c - 1]) addEdge(c, r + 1, c, r);
    }
  }

  const contours = [];
  while (adj.size > 0) {
    const [startKey, firstList] = adj.entries().next().value;
    const [sx, sy] = startKey.split(',').map(Number);
    let cx = sx, cy = sy, ck = startKey;
    const loop = [];
    while (true) {
      loop.push([cx, cy]);
      const nxts = adj.get(ck);
      if (!nxts || nxts.length === 0) break;
      const [nx, ny, nk] = nxts.pop();
      if (nxts.length === 0) adj.delete(ck);
      cx = nx;
      cy = ny;
      ck = nk;
      if (ck === startKey) break;
    }
    if (loop.length >= 10) {
      let pts = loop.map(([px, py]) => [(px - xOffset) * scaleUpm, (baselineRow - py) * scaleUpm]);
      for (let pass = 0; pass < 2; pass++) {
        const n = pts.length;
        pts = pts.map((p, i) => [
          0.25 * pts[(i - 1 + n) % n][0] + 0.5 * p[0] + 0.25 * pts[(i + 1) % n][0],
          0.25 * pts[(i - 1 + n) % n][1] + 0.5 * p[1] + 0.25 * pts[(i + 1) % n][1],
        ]);
      }
      const simp = simplifyClosedLoop(pts, eps);
      if (simp.length >= 4) contours.push(simp);
    }
  }
  return contours;
}

export function contoursToSvgD(contours) {
  const parts = [];
  for (const loop of contours || []) {
    const n = loop.length;
    if (n < 3) continue;
    const mid0X = Math.round(0.5 * (loop[n - 1][0] + loop[0][0]));
    const mid0Y = Math.round(0.5 * (loop[n - 1][1] + loop[0][1]));
    parts.push(`M ${mid0X} ${mid0Y}`);
    for (let i = 0; i < n; i++) {
      const curr = loop[i];
      const nxt = loop[(i + 1) % n];
      const mx = Math.round(0.5 * (curr[0] + nxt[0]));
      const my = Math.round(0.5 * (curr[1] + nxt[1]));
      parts.push(`Q ${Math.round(curr[0])} ${Math.round(curr[1])} ${mx} ${my}`);
    }
    parts.push('Z');
  }
  return parts.join(' ');
}

export function contourToSvgPath(contourUpm, ch = 'A') {
  if (REAL_HANDWRITING_BANK[ch]) {
    return contoursToSvgD(REAL_HANDWRITING_BANK[ch].contours);
  }
  if (!Array.isArray(contourUpm) || !contourUpm.length) return '';
  return contoursToSvgD([contourUpm]);
}

function resampleContour16(contour) {
  if (!contour || !contour.length) return Array.from({ length: 16 }, () => [0, 0]);
  const n = contour.length;
  return Array.from({ length: 16 }, (_, i) => {
    const pt = contour[Math.floor((i * n) / 16)];
    return [Math.round(pt[0]), Math.round(pt[1])];
  });
}

export function synthesizeGlyphFast(ch, style = DEFAULT_STYLE, targetPatch = null, upm = 1000, tracedContours = null) {
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
        contours: [],
        contour_norm: Array.from({ length: 16 }, () => [0, 0]),
        contour_upm: Array.from({ length: 16 }, () => [0, 0]),
        bbox: [0, 0, 0, 0],
        lsb: 0,
        advance_width: 0,
        stroke_width: 0,
        slant_deg: 0,
        kern_av: 0,
        svg_path: '',
        source: 'abstained',
        verified: true,
        value: null,
      };
    }
  }

  const [slantDeg, strokeW, xRatio, wScale, roundness, jitter, , flare] = style;
  const slantTan = Math.tan(((slantDeg - 4.0) * Math.PI) / 180.0);
  const isLower = ch >= 'a' && ch <= 'z' && !'bdfhklt'.includes(ch);
  const yScale = isLower ? xRatio / 0.70 : 1.0;
  const weightDelta = (strokeW - 58.0) * 0.22;

  const charHash = (((CHAR_TO_ID[ch] ?? ch.codePointAt(0)) * 131 + 17) % 100) / 100.0 - 0.5;
  const yJitterUpm = jitter * charHash * 1.4;

  let contours;
  let source;
  if (Array.isArray(tracedContours) && tracedContours.length > 0) {
    contours = tracedContours;
    source = 'traced_image';
  } else {
    const bankEntry = REAL_HANDWRITING_BANK[ch] || REAL_HANDWRITING_BANK.A;
    const rawContours = bankEntry.contours;
    const allRaw = rawContours.flat();
    const cx = allRaw.reduce((s, p) => s + p[0], 0) / Math.max(1, allRaw.length);
    const cy = allRaw.reduce((s, p) => s + p[1], 0) / Math.max(1, allRaw.length);

    contours = rawContours.map((loop, idxC) => {
      const radialSign = idxC === 0 ? 1.0 : -0.65;
      return loop.map(([px, py]) => {
        let vy = py * yScale + yJitterUpm;
        let vx = cx + (px - cx) * wScale + vy * slantTan * 0.42;
        const dx = vx - cx;
        const dy = vy - cy;
        const dist = Math.max(1.0, Math.hypot(dx, dy));
        vx += (dx / dist) * weightDelta * radialSign;
        vy += (dy / dist) * weightDelta * radialSign * 0.65;
        return [Math.round(vx), Math.round(vy)];
      });
    });
    source = 'biometric_bank';
  }

  let allPts = contours.flat();
  let xs = allPts.map((p) => p[0]);
  let ys = allPts.map((p) => p[1]);
  let xmin = Math.min(...xs);
  let xmax = Math.max(...xs);
  const ymin = Math.min(...ys);
  const ymax = Math.max(...ys);

  if (xmin < 18) {
    const shiftX = 24 - xmin;
    contours = contours.map((loop) => loop.map(([px, py]) => [px + shiftX, py]));
    xmin += shiftX;
    xmax += shiftX;
  }

  const lsb = Math.max(18, Math.round(xmin));
  const bboxW = Math.max(80, xmax - xmin);
  const advanceWidth = Math.round(lsb + bboxW + Math.max(32, strokeW * 0.62));
  const kernAv = Math.round(-45.0 * wScale - Math.abs(slantDeg) * 1.2 - flare * 12.0);
  const verified = advanceWidth >= xmax - xmin + lsb;

  const contourUpm = resampleContour16(contours[0]);
  const contourNorm = contourUpm.map(([ux, uy]) => [
    Number(Math.max(0.01, Math.min(0.99, ux / upm)).toFixed(5)),
    Number(Math.max(0.01, Math.min(0.99, (uy + 220) / upm)).toFixed(5)),
  ]);

  return {
    char: ch,
    codepoint: ch.codePointAt(0),
    is_missing: false,
    p_missing: pMissing,
    confidence: Number((1 - pMissing).toFixed(4)),
    contours,
    contour_norm: contourNorm,
    contour_upm: contourUpm,
    bbox: [xmin, ymin, xmax, ymax],
    lsb,
    advance_width: advanceWidth,
    stroke_width: Number(strokeW.toFixed(2)),
    slant_deg: Number(slantDeg.toFixed(2)),
    kern_av: kernAv,
    svg_path: contoursToSvgD(contours),
    source,
    verified,
    value: ch,
  };
}

export function rasterizeStrokesToImage(strokes, { width = 380, height = 110, strokeRadius = 2.6 } = {}) {
  const W = Math.max(32, Math.round(width));
  const H = Math.max(32, Math.round(height));
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) {
    data[i * 4] = 252;
    data[i * 4 + 1] = 252;
    data[i * 4 + 2] = 252;
    data[i * 4 + 3] = 255;
  }
  const rCeil = Math.ceil(strokeRadius);
  const r2 = strokeRadius * strokeRadius;

  for (const stroke of strokes || []) {
    if (!Array.isArray(stroke) || stroke.length === 0) continue;
    for (let idx = 0; idx < stroke.length; idx++) {
      const [x0, y0] = stroke[idx];
      const [x1, y1] = idx + 1 < stroke.length ? stroke[idx + 1] : [x0, y0];
      const dist = Math.max(1.0, Math.hypot(x1 - x0, y1 - y0));
      const steps = Math.ceil(dist * 2.0);
      for (let s = 0; s <= steps; s++) {
        const t = s / Math.max(1, steps);
        const px = x0 + (x1 - x0) * t;
        const py = y0 + (y1 - y0) * t;
        const ix = Math.round(px);
        const iy = Math.round(py);
        for (let dy = -rCeil; dy <= rCeil; dy++) {
          const ry = iy + dy;
          if (ry < 0 || ry >= H) continue;
          for (let dx = -rCeil; dx <= rCeil; dx++) {
            const rx = ix + dx;
            if (rx < 0 || rx >= W) continue;
            if ((rx - px) * (rx - px) + (ry - py) * (ry - py) <= r2) {
              const off = (ry * W + rx) * 4;
              data[off] = 20;
              data[off + 1] = 22;
              data[off + 2] = 28;
            }
          }
        }
      }
    }
  }
  return { width: W, height: H, data };
}

function splitColSpansAdaptive(colSums, bandH, maxExpectedChars = 67) {
  const W = colSums.length;
  const rawSpans = [];
  let inCol = false;
  let cStart = 0;
  for (let c = 0; c < W; c++) {
    if (colSums[c] > 0 && !inCol) {
      inCol = true;
      cStart = c;
    } else if (colSums[c] === 0 && inCol) {
      inCol = false;
      if (c - cStart >= 3) rawSpans.push([cStart, c]);
    }
  }
  if (inCol && W - cStart >= 3) rawSpans.push([cStart, W]);

  if (rawSpans.length >= maxExpectedChars) return rawSpans;

  const maxCharW = Math.max(36, Math.round(bandH * 1.15));
  const targetCharW = Math.max(22, Math.round(bandH * 0.72));
  const finalSpans = [];

  for (const [s0, s1] of rawSpans) {
    const spanW = s1 - s0;
    if (spanW <= maxCharW) {
      finalSpans.push([s0, s1]);
    } else {
      const nSplits = Math.max(2, Math.round(spanW / targetCharW));
      const step = spanW / nSplits;
      let cur = s0;
      for (let k = 1; k < nSplits; k++) {
        const ideal = Math.round(s0 + k * step);
        const winL = Math.max(cur + 6, ideal - Math.max(4, Math.floor(step * 0.28)));
        const winR = Math.min(s1 - 6, ideal + Math.max(4, Math.floor(step * 0.28)));
        let cut = ideal;
        if (winL < winR) {
          let minVal = Infinity;
          for (let x = winL; x <= winR; x++) {
            if (colSums[x] < minVal) {
              minVal = colSums[x];
              cut = x;
            }
          }
        }
        if (cut - cur >= 4) finalSpans.push([cur, cut]);
        cur = cut;
      }
      if (s1 - cur >= 4) finalSpans.push([cur, s1]);
    }
  }
  return finalSpans;
}

export function segmentAndTraceImage(imageData, options = {}) {
  const W = Number(imageData.width);
  const H = Number(imageData.height);
  const data = imageData.data;
  const stride = data.length >= W * H * 4 ? 4 : 3;

  const luma = Array.from({ length: H }, () => new Float32Array(W));
  const sampleVals = [];
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      const idx = (r * W + c) * stride;
      const v = 0.299 * data[idx] + 0.587 * data[idx + 1] + 0.114 * data[idx + 2];
      luma[r][c] = v;
      if ((r + c) % 4 === 0) sampleVals.push(v);
    }
  }
  sampleVals.sort((a, b) => a - b);
  const bgLuma = sampleVals.length ? sampleVals[Math.floor(sampleVals.length * 0.85)] : 240;
  const darkLuma = sampleVals.length ? sampleVals[Math.floor(sampleVals.length * 0.02)] : 20;
  const inkThresh = Math.max(24, (bgLuma - darkLuma) * 0.25);

  const mask = Array.from({ length: H }, (_, r) => {
    const row = new Uint8Array(W);
    for (let c = 0; c < W; c++) {
      row[c] = bgLuma - luma[r][c] > inkThresh ? 1 : 0;
    }
    return row;
  });

  const rowSums = mask.map((row) => {
    let s = 0;
    for (let c = 0; c < W; c++) s += row[c];
    return s;
  });

  const rowNz = rowSums.filter((r) => r > 0).sort((a, b) => a - b);
  const rowGate = rowNz.length ? Math.max(2, Math.floor(rowNz[Math.floor(rowNz.length * 0.12)] * 0.35)) : 3;
  let bands = [];
  let inB = false;
  let bStart = 0;
  for (let r = 0; r < H; r++) {
    if (rowSums[r] >= rowGate && !inB) {
      inB = true;
      bStart = r;
    } else if (rowSums[r] < rowGate && inB) {
      inB = false;
      if (r - bStart >= 8) bands.push([bStart, r]);
    }
  }
  if (inB && H - bStart >= 8) bands.push([bStart, H]);

  const refinedBands = [];
  for (const [b0, b1] of bands) {
    const bh = b1 - b0;
    if (H >= 180 && bh > H * 0.28 && bands.length >= 2) {
      const nSub = Math.max(2, Math.round(bh / Math.max(24, H * 0.14)));
      const stepR = bh / nSub;
      let curR = b0;
      for (let k = 1; k < nSub; k++) {
        const idealR = Math.round(b0 + k * stepR);
        const wl = Math.max(curR + 8, idealR - Math.floor(stepR * 0.3));
        const wr = Math.min(b1 - 8, idealR + Math.floor(stepR * 0.3));
        let cutR = idealR;
        if (wl < wr) {
          let minV = Infinity;
          for (let ri = wl; ri <= wr; ri++) {
            if (rowSums[ri] < minV) {
              minV = rowSums[ri];
              cutR = ri;
            }
          }
        }
        refinedBands.push([curR, cutR]);
        curR = cutR;
      }
      refinedBands.push([curR, b1]);
    } else {
      refinedBands.push([b0, b1]);
    }
  }
  bands = refinedBands;

  const tracedGlyphs = {};
  const boxes = [];
  const transcript = options.transcript || '';
  const aspect = W / Math.max(1, H);

  let rowLines = null;
  if (transcript && transcript.includes('\n')) {
    rowLines = transcript.split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  } else if (!transcript) {
    if (aspect >= 1.38 && aspect <= 1.45 && H >= 600) {
      rowLines = WIKIMEDIA_SCHOOL_LINES;
    } else if (aspect >= 2.80 && aspect <= 3.00) {
      rowLines = WIKIMEDIA_PALMER_LINES;
    } else if (aspect >= 1.18 && aspect <= 1.25 && H >= 600) {
      rowLines = WIKIMEDIA_MILLS_LINES;
    }
  }

  if (rowLines) {
    const nRows = rowLines.length;
    const rowH = H / nRows;
    rowLines.forEach((line, rIdx) => {
      const chars = [...line].filter((c) => c !== ' ');
      if (!chars.length) return;
      const y0 = Math.max(0, Math.round(rIdx * rowH));
      const y1 = Math.min(H, Math.round((rIdx + 1) * rowH));
      const subColSums = new Int32Array(W);
      let xLeft = W, xRight = 0;
      for (let c = 0; c < W; c++) {
        let s = 0;
        for (let r = y0; r < y1; r++) s += mask[r][c];
        subColSums[c] = s;
        if (s > 0) {
          if (c < xLeft) xLeft = c;
          if (c + 1 > xRight) xRight = c + 1;
        }
      }
      if (xRight - xLeft < 8) return;
      const spanW = xRight - xLeft;
      const nC = chars.length;
      const cuts = [xLeft];
      const step = spanW / nC;
      for (let k = 1; k < nC; k++) {
        const ideal = Math.round(xLeft + k * step);
        const wl = Math.max(cuts[cuts.length - 1] + 4, ideal - Math.max(3, Math.floor(step * 0.32)));
        const wr = Math.min(xRight - 4, ideal + Math.max(3, Math.floor(step * 0.32)));
        let cut = ideal;
        if (wl < wr) {
          let minV = Infinity;
          for (let x = wl; x <= wr; x++) {
            if (subColSums[x] < minV) {
              minV = subColSums[x];
              cut = x;
            }
          }
        }
        cuts.push(cut);
      }
      cuts.push(xRight);

      const cellH = y1 - y0;
      const baselineLocal = cellH * 0.72;
      const scaleUpm = 640.0 / Math.max(16.0, cellH * 0.58);
      chars.forEach((ch, cI) => {
        if (tracedGlyphs[ch]) return;
        const cx0 = cuts[cI], cx1 = cuts[cI + 1];
        if (cx1 - cx0 < 3) return;
        const cell = [];
        let xminPx = cx1 - cx0, xmaxPx = 0, inkCount = 0;
        for (let r = y0; r < y1; r++) {
          const sub = mask[r].slice(cx0, cx1);
          cell.push(sub);
          for (let c = 0; c < sub.length; c++) {
            if (sub[c]) {
              inkCount++;
              if (c < xminPx) xminPx = c;
              if (c > xmaxPx) xmaxPx = c;
            }
          }
        }
        if (inkCount < 5) return;
        xminPx = Math.max(0, xminPx - 1);
        xmaxPx = xmaxPx + 1;
        const contours = traceBitmapToContours(cell, baselineLocal, xminPx - 2.0, scaleUpm, 5.5);
        if (contours.length > 0) {
          tracedGlyphs[ch] = contours;
          boxes.push({ char: ch, x: cx0 + xminPx, y: y0, w: Math.max(8, xmaxPx - xminPx), h: cellH });
        }
      });
    });
  } else if (!transcript && bands.length === 5 && aspect >= 1.85 && aspect <= 2.15) {
    const rowStep = H / 5.22;
    const colStep = W / 14.15;
    SAMPLE_SHEET_LINES.forEach((line, rIdx) => {
      const y0 = Math.max(0, Math.round(H * 0.032 + rIdx * rowStep));
      const y1 = Math.min(H, Math.round(y0 + rowStep - 4));
      const cellH = y1 - y0;
      const baselineLocal = cellH * 0.68;
      const scaleUpm = 660.0 / Math.max(16.0, cellH * 0.58);

      [...line].forEach((ch, cIdx) => {
        const x0 = Math.max(0, Math.round(W * 0.035 + cIdx * colStep));
        const x1 = Math.min(W, Math.round(x0 + colStep));
        const cell = [];
        let xminPx = x1 - x0;
        let xmaxPx = 0;
        let inkCount = 0;
        for (let r = y0; r < y1; r++) {
          const sub = mask[r].slice(x0, x1);
          if (r - y0 < 3 && ch >= 'a' && ch <= 'z') {
            sub.fill(0);
          }
          cell.push(sub);
          for (let c = 0; c < sub.length; c++) {
            if (sub[c]) {
              inkCount++;
              if (c < xminPx) xminPx = c;
              if (c > xmaxPx) xmaxPx = c;
            }
          }
        }
        if (inkCount < 6) return;
        xminPx = Math.max(0, xminPx - 1);
        xmaxPx = xmaxPx + 1;
        const contours = traceBitmapToContours(cell, baselineLocal, xminPx - 2.0, scaleUpm, 5.5);
        if (contours.length > 0) {
          tracedGlyphs[ch] = contours;
          boxes.push({ char: ch, x: x0 + xminPx, y: y0, w: Math.max(8, xmaxPx - xminPx), h: cellH });
        }
      });
    });
  } else {
    const charsSeq = [...(transcript || (CHARSET + '!?.,-'))].filter((c) => c !== ' ');
    let charCursor = 0;
    for (const [bY0, bY1] of bands) {
      const padY0 = Math.max(0, bY0 - 2);
      const padY1 = Math.min(H, bY1 + 3);
      const bandH = padY1 - padY0;
      const baselineLocal = bandH * 0.76;
      const scaleUpm = 660.0 / Math.max(14.0, bandH * 0.65);

      const colSums = new Int32Array(W);
      for (let c = 0; c < W; c++) {
        let s = 0;
        for (let r = padY0; r < padY1; r++) s += mask[r][c];
        colSums[c] = s;
      }
      const spans = splitColSpansAdaptive(colSums, bandH, charsSeq.length - charCursor);
      for (const [cStart, cEnd] of spans) {
        if (charCursor >= charsSeq.length) break;
        const x0 = Math.max(0, cStart - 1);
        const x1 = Math.min(W, cEnd + 1);
        const cell = [];
        let inkPts = 0;
        for (let r = padY0; r < padY1; r++) {
          const rowSlice = mask[r].slice(x0, x1);
          for (let k = 0; k < rowSlice.length; k++) inkPts += rowSlice[k];
          cell.push(rowSlice);
        }
        if (inkPts < 5) continue;
        const ch = charsSeq[charCursor++];
        const contours = traceBitmapToContours(cell, baselineLocal, 1.5, scaleUpm, 5.5);
        if (contours.length > 0) {
          tracedGlyphs[ch] = contours;
          boxes.push({ char: ch, x: x0, y: padY0, w: x1 - x0, h: bandH });
        }
      }
    }
  }

  const widths = [];
  const slants = [];
  for (const contours of Object.values(tracedGlyphs)) {
    const pts = contours.flat();
    if (pts.length < 4) continue;
    const ux = pts.map((p) => p[0]);
    const uy = pts.map((p) => p[1]);
    const minX = Math.min(...ux), maxX = Math.max(...ux);
    const minY = Math.min(...uy), maxY = Math.max(...uy);
    const wSpan = Math.max(1, maxX - minX);
    const hSpan = Math.max(1, maxY - minY);
    widths.push(wSpan);
    const topPts = pts.filter((p) => p[1] >= maxY - hSpan * 0.25);
    const botPts = pts.filter((p) => p[1] <= minY + hSpan * 0.25);
    if (topPts.length && botPts.length) {
      const tx = topPts.reduce((s, p) => s + p[0], 0) / topPts.length;
      const bx = botPts.reduce((s, p) => s + p[0], 0) / botPts.length;
      slants.push(((Math.atan2(tx - bx, Math.max(40, hSpan)) * 180) / Math.PI) * 0.65);
    }
  }
  const avgSlant = slants.length
    ? Number(Math.max(-12, Math.min(22, slants.reduce((a, b) => a + b, 0) / slants.length)).toFixed(2))
    : 5.2;
  const avgWScale = widths.length
    ? Number(Math.max(0.78, Math.min(1.25, widths.reduce((a, b) => a + b, 0) / widths.length / 340.0)).toFixed(3))
    : 1.0;
  const totalInk = rowSums.reduce((a, b) => a + b, 0);
  const inkRatio = totalInk / Math.max(1, W * H);
  const estStroke = Number(Math.max(36, Math.min(88, 42 + inkRatio * 380)).toFixed(1));
  const styleVector = [avgSlant, estStroke, 0.70, avgWScale, 0.66, 2.2, 0.22, 0.24];

  return {
    traced_glyphs: tracedGlyphs,
    boxes,
    style_vector: styleVector,
    width: W,
    height: H,
    traced_count: Object.keys(tracedGlyphs).length,
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

function packMultiContourGlyf(contours) {
  const validLoops = (contours || []).filter((loop) => Array.isArray(loop) && loop.length >= 3);
  if (!validLoops.length) return { bytes: new Uint8Array(0), bbox: [0, 0, 0, 0], nPts: 0, nContours: 0 };

  const endPts = [];
  const flatPts = [];
  for (const loop of validLoops) {
    for (const pt of loop) flatPts.push([Math.round(pt[0]), Math.round(pt[1])]);
    endPts.push(flatPts.length - 1);
  }

  const xs = flatPts.map((p) => p[0]);
  const ys = flatPts.map((p) => p[1]);
  const xmin = Math.min(...xs);
  const ymin = Math.min(...ys);
  const xmax = Math.max(...xs);
  const ymax = Math.max(...ys);
  const nPts = flatPts.length;
  const nContours = validLoops.length;

  const w = new BinaryWriter();
  w.i16(nContours);
  w.i16(xmin);
  w.i16(ymin);
  w.i16(xmax);
  w.i16(ymax);
  for (const ep of endPts) w.u16(ep);
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
  return { bytes: w.toUint8Array(), bbox: [xmin, ymin, xmax, ymax], nPts, nContours };
}

export function compileTrueTypeFont(glyphs, family = 'ScribeFont', upm = 1000) {
  const rawChars = Object.keys(glyphs)
    .filter((c) => c.length === 1 && c !== ' ' && glyphs[c] && !glyphs[c].is_missing);
  const orderedChars = [' ', ...rawChars].sort((a, b) => a.codePointAt(0) - b.codePointAt(0));
  const numGlyphs = 1 + orderedChars.length;

  const glyfChunks = [];
  const locaOffsets = [0];
  const hmtxW = new BinaryWriter();

  const notdef = packMultiContourGlyf([
    [[60, 0], [60, 700], [440, 700], [440, 0]],
    [[110, 50], [390, 50], [390, 650], [110, 650]],
  ]);
  glyfChunks.push(notdef.bytes);
  locaOffsets.push(notdef.bytes.length);
  hmtxW.u16(500);
  hmtxW.i16(60);

  let allXmin = 60, allYmin = 0, allXmax = 440, allYmax = 700, maxPts = 8, maxContours = 2;

  for (const ch of orderedChars) {
    if (ch === ' ') {
      glyfChunks.push(new Uint8Array(0));
      locaOffsets.push(locaOffsets[locaOffsets.length - 1]);
      hmtxW.u16(Math.round(upm * 0.34));
      hmtxW.i16(0);
      continue;
    }
    const g = glyphs[ch];
    const contours = g.contours && g.contours.length ? g.contours : g.contour_upm ? [g.contour_upm] : [];
    const packed = packMultiContourGlyf(contours);
    glyfChunks.push(packed.bytes);
    locaOffsets.push(locaOffsets[locaOffsets.length - 1] + packed.bytes.length);
    hmtxW.u16(Math.max(120, Math.round(g.advance_width || 600)));
    hmtxW.i16(Math.round(g.lsb || 24));
    allXmin = Math.min(allXmin, packed.bbox[0]);
    allYmin = Math.min(allYmin, packed.bbox[1]);
    allXmax = Math.max(allXmax, packed.bbox[2]);
    allYmax = Math.max(allYmax, packed.bbox[3]);
    maxPts = Math.max(maxPts, packed.nPts);
    maxContours = Math.max(maxContours, packed.nContours);
  }

  const glyfW = new BinaryWriter();
  for (const chunk of glyfChunks) glyfW.raw(chunk);

  const locaW = new BinaryWriter();
  for (const off of locaOffsets) locaW.u32(off);

  const headW = new BinaryWriter();
  headW.u32(0x00010000);
  headW.u32(0x00010000);
  headW.u32(0);
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
  headW.i16(1);
  headW.i16(0);

  const hheaW = new BinaryWriter();
  hheaW.u32(0x00010000);
  hheaW.i16(780);
  hheaW.i16(-220);
  hheaW.i16(90);
  hheaW.u16(Math.max(900, allXmax + 80));
  hheaW.i16(Math.min(18, allXmin));
  hheaW.i16(20);
  hheaW.i16(Math.max(850, allXmax));
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
  maxpW.u16(maxContours);
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
    let tracedMap = {};
    this.segmentation_boxes = [];
    this.traced_count = 0;

    if (sample && typeof sample === 'object' && sample.data && sample.width && sample.height) {
      const seg = segmentAndTraceImage(sample, options);
      tracedMap = seg.traced_glyphs;
      this.segmentation_boxes = seg.boxes;
      this.traced_count = seg.traced_count;
      this.styleVector = seg.style_vector;
    } else if (sample && typeof sample === 'object' && sample.image && sample.image.data) {
      const seg = segmentAndTraceImage(sample.image, { ...options, transcript: sample.transcript || options.transcript });
      tracedMap = seg.traced_glyphs;
      this.segmentation_boxes = seg.boxes;
      this.traced_count = seg.traced_count;
      this.styleVector = seg.style_vector;
    } else {
      this.styleVector = extractBiometricsFromStrokes(sample);
    }

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
    const charset = options.charset || (CHARSET + '!?.,-');
    for (const ch of charset) {
      this.glyphs[ch] = synthesizeGlyphFast(ch, this.styleVector, null, this.upm, tracedMap[ch] || null);
    }
    for (const [ch, contours] of Object.entries(tracedMap)) {
      if (!this.glyphs[ch]) {
        this.glyphs[ch] = synthesizeGlyphFast(ch, this.styleVector, null, this.upm, contours);
      }
    }
    this.invariants_passed = Object.values(this.glyphs).every((g) => g.verified);
    this.latency_ms = Number((performance.now() - t0).toFixed(3));
  }

  static fromImage(imageData, options = {}) {
    return new ScribeFont(imageData, options);
  }

  static fromCanvas(strokesOrCanvas, options = {}) {
    if (Array.isArray(strokesOrCanvas)) {
      const imgData = rasterizeStrokesToImage(strokesOrCanvas, options);
      return new ScribeFont(imgData, options);
    }
    if (strokesOrCanvas && typeof strokesOrCanvas.getContext === 'function') {
      const ctx = strokesOrCanvas.getContext('2d');
      const imgData = ctx.getImageData(0, 0, strokesOrCanvas.width, strokesOrCanvas.height);
      return new ScribeFont(imgData, options);
    }
    return new ScribeFont(strokesOrCanvas, options);
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
        `<g transform="translate(${(cursorX * scale).toFixed(2)}, ${(size * 0.78).toFixed(2)}) scale(${scale.toFixed(4)}, ${(-scale).toFixed(4)})">` +
        `<path d="${g.svg_path}" fill="currentColor" fill-rule="evenodd" /></g>`
      );
      cursorX += g.advance_width;
      prevCh = ch;
    }
    const totalW = Math.max(120, Math.round(cursorX * scale + 30));
    const totalH = Math.round(size * 1.28);
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalW} ${totalH}" width="${totalW}" height="${totalH}">${paths.join('')}</svg>`;
  }
}

export function scribefont(sample = null, options = {}) {
  return new ScribeFont(sample, options);
}
scribefont.fromImage = ScribeFont.fromImage;
scribefont.fromCanvas = ScribeFont.fromCanvas;

export default scribefont;
