---
title: DOM-Free Text Layout and Measurement
category: reference
tags: [web-frontend, text-layout, canvas, performance, line-breaking, reflow, pretext, virtualization, cjk]
---

# DOM-Free Text Layout and Measurement

Measuring and laying out text without triggering browser DOM reflow. Critical for virtualized lists, canvas renderers, server-side rendering, and real-time layout validation in CI pipelines.

## The DOM Measurement Problem

Browser text measurement via DOM causes layout reflow:

```javascript
// ❌ Each call triggers reflow (expensive):
el.innerText = text;
const height = el.getBoundingClientRect().height; // layout reflow
// Cascading reflows: N components × reflow = frame budget exceeded

// Also expensive:
el.offsetHeight;    // layout
el.scrollHeight;    // layout
window.getComputedStyle(el).height;  // layout (sometimes)
```

**Impact:** In virtualized lists with 1,000+ items, DOM-based height estimation blocks scrolling. In chat UIs, precise pre-render height enables smooth scroll-to-bottom without jumping.

## Canvas API: Browser-Native Measurement

The only reflow-free text measurement in browsers is `CanvasRenderingContext2D.measureText()`:

```javascript
const canvas = new OffscreenCanvas(1, 1); // no DOM insertion needed
const ctx = canvas.getContext('2d');
ctx.font = '16px system-ui, sans-serif';

const metrics = ctx.measureText('Hello world');
console.log(metrics.width);                          // exact pixel width
console.log(metrics.actualBoundingBoxAscent);        // above baseline
console.log(metrics.actualBoundingBoxDescent);       // below baseline
// Note: no height property - must compute from ascent + descent
```

**Limitations:**
- Returns only single-line metrics - no multi-line wrapping
- No access to individual glyph positions
- Doesn't handle complex scripts (Arabic shaping, Thai syllable breaking) correctly without additional processing
- Font must be loaded before measurement (use `document.fonts.ready` or `FontFace.load()`)

## Two-Phase Layout Architecture

Separate the "prepare" (expensive, once) from "layout" (cheap, per-resize) phases:

```typescript
interface PreparedText {
  segments: TextSegment[];   // pre-analyzed break opportunities
  widthCache: Map<string, number>;  // character/word -> measured width
  font: string;
}

// Phase 1: prepare (once per text + font combination)
function prepare(text: string, font: string): PreparedText {
  const ctx = offscreenCtx(font);
  const segmenter = new Intl.Segmenter('auto', { granularity: 'word' });
  const segments = [...segmenter.segment(text)];
  
  const widthCache = new Map<string, number>();
  for (const seg of segments) {
    if (!widthCache.has(seg.segment)) {
      widthCache.set(seg.segment, ctx.measureText(seg.segment).width);
    }
  }
  return { segments, widthCache, font };
}

// Phase 2: layout (called on every resize, no DOM, pure arithmetic)
function layout(
  prepared: PreparedText,
  maxWidth: number,
  lineHeight: number
): { lines: string[], height: number } {
  const lines: string[] = [];
  let currentLine = '';
  let currentWidth = 0;
  
  for (const seg of prepared.segments) {
    const segWidth = prepared.widthCache.get(seg.segment) ?? 0;
    
    if (currentWidth + segWidth > maxWidth && currentLine !== '') {
      lines.push(currentLine.trimEnd());
      currentLine = seg.segment;
      currentWidth = segWidth;
    } else {
      currentLine += seg.segment;
      currentWidth += segWidth;
    }
  }
  
  if (currentLine) lines.push(currentLine.trimEnd());
  
  return { lines, height: lines.length * lineHeight };
}
```

## Intl.Segmenter for Unicode-Correct Word Breaking

`Intl.Segmenter` handles what manual splitting misses:

```javascript
// ❌ Naive: breaks CJK, emoji, Thai
const words = text.split(' ');  // breaks "你好" -> ["你好"] (no spaces)

// ✓ Correct: locale-aware segmentation
const segmenter = new Intl.Segmenter('zh', { granularity: 'word' });
const words = [...segmenter.segment('你好世界')];
// [{segment: '你好', isWordLike: true}, {segment: '世界', isWordLike: true}]

// For mixed content, use 'auto' locale:
const segmenter = new Intl.Segmenter('auto', { granularity: 'grapheme' });
// Correctly handles: emoji sequences, combining characters, ZWJ sequences
```

## Line Break Rules by Type

| Break type | Unicode | Behavior |
|------------|---------|----------|
| Normal word break | U+0020 SPACE | Collapses with adjacent spaces |
| Preserved space | NBSP U+00A0 | Never collapses, breaks line only if no alternative |
| Zero-width break | U+200B ZWSP | Allows break, renders nothing |
| Zero-width joiner | U+200D ZWJ | Prevents break between characters |
| Soft hyphen | U+00AD SHY | Insert hyphen only when breaking here |
| Hard break | U+000A LF | Always breaks |
| Tab | U+0009 | Expand to next tab stop |

```javascript
// CJK kinsoku shori (Japanese line break rules)
// Characters that cannot start a line:
const CANNOT_START = '）〕】』」…—';
// Characters that cannot end a line:
const CANNOT_END = '（〔【『「';

function isLineBreakAllowed(before: string, after: string): boolean {
  if (CANNOT_END.includes(before)) return false;
  if (CANNOT_START.includes(after)) return false;
  return true;
}
```

## Variable-Width Line Layout

Each line has its own maximum width (text flowing around an image):

```typescript
interface LineConstraints {
  offset: number;  // horizontal offset from left
  width: number;   // available width for this line
}

function layoutVariableWidth(
  prepared: PreparedText,
  lineConstraints: LineConstraints[],  // one entry per line
  defaultWidth: number,
  lineHeight: number
): { lines: PositionedLine[] } {
  const lines: PositionedLine[] = [];
  let lineIndex = 0;
  let currentLine = '';
  let currentWidth = 0;
  
  const getConstraint = (i: number) => 
    lineConstraints[i] ?? { offset: 0, width: defaultWidth };
  
  for (const seg of prepared.segments) {
    const constraint = getConstraint(lineIndex);
    const segWidth = prepared.widthCache.get(seg.segment) ?? 0;
    
    if (currentWidth + segWidth > constraint.width) {
      lines.push({ text: currentLine, x: constraint.offset, y: lineIndex * lineHeight });
      lineIndex++;
      currentLine = seg.segment;
      currentWidth = segWidth;
    } else {
      currentLine += seg.segment;
      currentWidth += segWidth;
    }
  }
  return { lines };
}
```

## Shrinkwrap / Balanced Text Width

Find optimal container width to minimize line count waste (balanced layout):

```typescript
function shrinkwrapWidth(
  prepared: PreparedText,
  minWidth: number,
  maxWidth: number,
  lineHeight: number,
  targetLines: number
): number {
  // Binary search for optimal width:
  let lo = minWidth, hi = maxWidth;
  
  while (hi - lo > 1) {
    const mid = Math.floor((lo + hi) / 2);
    const { lines } = layout(prepared, mid, lineHeight);
    
    if (lines.length <= targetLines) {
      hi = mid;  // can fit in fewer px
    } else {
      lo = mid;  // need more width
    }
  }
  
  return hi;
}
```

## Rendering Targets

### Canvas Rendering

```javascript
function renderLines(ctx: CanvasRenderingContext2D, lines: string[], 
                      x: number, y: number, lineHeight: number) {
  ctx.save();
  ctx.font = '16px system-ui';
  ctx.fillStyle = '#000';
  ctx.textBaseline = 'alphabetic';
  
  lines.forEach((line, i) => {
    ctx.fillText(line, x, y + i * lineHeight);
  });
  
  ctx.restore();
}
```

### SVG Rendering

```javascript
function renderSVGLines(lines: string[], x: number, y: number, lineHeight: number): string {
  return lines.map((line, i) =>
    `<text x="${x}" y="${y + i * lineHeight}" font-size="16" font-family="system-ui">${
      line.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    }</text>`
  ).join('\n');
}
```

### DOM Rendering (with pre-computed height)

```javascript
// With known height, no reflowing during scroll:
function renderVirtualItem(lines: string[], height: number): HTMLElement {
  const div = document.createElement('div');
  div.style.height = `${height}px`;
  div.style.contain = 'strict';  // prevent layout bleed
  div.textContent = lines.join('\n');
  return div;
}
```

## CI Pipeline: Layout Validation

Test that AI-generated UIs don't overflow buttons or truncate labels - without a browser:

```typescript
import { prepare, layout } from 'pretext'; // or your implementation

function validateButtonLabel(label: string, buttonWidthPx: number): boolean {
  const prepared = prepare(label, '14px system-ui');
  const { lines } = layout(prepared, buttonWidthPx - 16, 20); // 16px padding
  return lines.length === 1;  // multi-line = overflow
}

// Jest test:
describe('Button label overflow', () => {
  const buttonWidth = 120;
  
  test.each([
    ['Submit', true],
    ['Submit Order to Cart', false],
    ['OK', true],
  ])('"%s" fits: %s', (label, expected) => {
    expect(validateButtonLabel(label, buttonWidth)).toBe(expected);
  });
});
```

## RTL Text Support

```javascript
// Detect text direction:
function getTextDirection(text: string): 'ltr' | 'rtl' {
  // Unicode bidi algorithm: check first strong character
  const RTL_CHARS = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/;
  return RTL_CHARS.test(text) ? 'rtl' : 'ltr';
}

// Canvas RTL rendering:
function renderRTL(ctx: CanvasRenderingContext2D, text: string, 
                    x: number, y: number, maxWidth: number) {
  ctx.direction = 'rtl';
  ctx.textAlign = 'right';
  ctx.fillText(text, x + maxWidth, y);  // anchor at right edge
}
```

## Gotchas

- **`measureText` requires loaded fonts** - if the page font hasn't loaded yet, Canvas measures with the fallback font and returns wrong widths. Always await `document.fonts.ready` before calling `prepare()`, or use `FontFace.load()` for dynamically loaded fonts. Measurements done before font load silently use wrong metrics
- **`measureText` width ≠ visual width for emoji and ZWJ sequences** - multi-codepoint emoji (e.g. family emoji `👨‍👩‍👧`) are measured as single glyphs in some environments but as multiple characters by `Intl.Segmenter`. Always segment first, then measure each segment, not each codepoint
- **CJK `word-break: keep-all` is not default** - in Korean, Chinese, and Japanese text, browsers allow line breaks between any two CJK characters by default. In some contexts (`keep-all`), breaks should only occur at spaces/punctuation. Your layout engine must implement this explicitly if needed

## Pretext Library

`github.com/chenglou/pretext` (41K+ stars, MIT) - reference implementation of DOM-free text layout by the author of React Motion and ReasonML. Handles 15+ languages, 8 break types, shrinkwrap, variable-width layout, rich inline flow. TypeScript, Bun runtime.

## See Also

- [[web-frontend/react-rendering-internals]] - React reconciler and DOM update batching
- [[web-frontend/css-box-model-and-layout]] - when DOM layout is acceptable
- [[web-frontend/js-dom-and-events]] - reflow triggers and batching with `requestAnimationFrame`
