export interface ScribeStyle {
  slant_deg: number;
  stroke_width: number;
  x_height_ratio: number;
  width_scale: number;
  roundness: number;
  baseline_jitter: number;
  contrast: number;
  serif_flare: number;
}

export interface ScribeGlyph {
  char: string;
  codepoint: number;
  is_missing: boolean;
  p_missing: number;
  confidence: number;
  contour_norm: [number, number][];
  contour_upm: [number, number][];
  bbox: [number, number, number, number];
  lsb: number;
  advance_width: number;
  stroke_width: number;
  slant_deg: number;
  kern_av: number;
  svg_path: string;
  verified: boolean;
  value: string | null;
}

export type ScribeScript =
  | 'latin'
  | 'devanagari'
  | 'sanskrit'
  | 'hindi'
  | 'kannada'
  | 'tamil'
  | 'telugu'
  | 'bengali'
  | 'multilingual';

export interface ScribeFontOptions {
  family?: string;
  upm?: number;
  charset?: string;
  script?: ScribeScript;
  transcript?: string;
}

export declare const DEVANAGARI_CHARSET: string;
export declare const KANNADA_CHARSET: string;
export declare const TAMIL_CHARSET: string;
export declare const TELUGU_CHARSET: string;
export declare const BENGALI_CHARSET: string;
export declare const INDIC_SCRIPTS: Record<string, string>;
export declare const SANSKRIT_SAMPLE_LINES: string[];
export declare const DEVANAGARI_SAMPLE_LINES: string[];
export declare function reorderIndicVisualOrder(text: string): string;

export declare class ScribeFont {
  family: string;
  upm: number;
  styleVector: number[];
  style: ScribeStyle;
  glyphs: Record<string, ScribeGlyph>;
  invariants_passed: boolean;
  latency_ms: number;
  constructor(sample?: unknown, options?: ScribeFontOptions);
  glyph(ch: string): ScribeGlyph;
  kerning(left: string, right: string): number;
  toTTF(): Uint8Array;
  toSVGFont(): string;
  renderSVG(text: string, options?: { size?: number }): string;
}

export declare function scribefont(sample?: unknown, options?: ScribeFontOptions): ScribeFont;
export declare function verifyTrueTypeBytes(ttfBytes: Uint8Array): {
  valid: boolean;
  checksum_ok: boolean;
  num_tables: number;
  tables: string[];
  byte_length: number;
};
export default scribefont;
