---
title: "DOM-freies Textlayout und Messung"
category: reference
tags: [web-frontend, text-layout, canvas, performance, line-breaking, reflow, pretext, virtualization, cjk]
level: 3
source_sha256: fcb534d8cf273d3a36907df5e27450524baa040880192d1583867549d8b40b26
translation: machine
translated_at: '2026-10-24'
---
# DOM-freies Textlayout und Messung {#dom-free-text-layout-and-measurement}

Text lässt sich messen und layouten, ohne einen Browser-DOM-Reflow auszulösen. Das ist entscheidend für virtualisierte Listen, Canvas-Renderer, Server-Side Rendering und die Validierung von Layouts in CI-Pipelines in Echtzeit.

## Das DOM-Messproblem {#the-dom-measurement-problem}

Die Textmessung im Browser über das DOM löst Layout-Reflows aus:

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

**Auswirkung:** In virtualisierten Listen mit über 1.000 Einträgen blockiert die DOM-basierte Höhenschätzung das Scrollen. In Chat-UIs ermöglicht eine präzise Höhe vor dem Rendern ein flüssiges Scrollen zum Ende, ohne dass die Ansicht springt.

## Canvas-API: Browser-native Messung {#canvas-api-browser-native-measurement}

Die einzige reflowfreie Textmessung im Browser ist `CanvasRenderingContext2D.measureText()`:

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

**Einschränkungen:**
- Liefert nur einzeilige Metriken, kein mehrzeiliges Umbrechen
- Kein Zugriff auf die Positionen einzelner Glyphen
- Komplexe Schriftsysteme (Arabisch mit Formschreibung, Thai mit Silbentrennung) werden ohne zusätzliche Verarbeitung nicht korrekt behandelt
- Die Schrift muss vor der Messung geladen sein (`document.fonts.ready` oder `FontFace.load()` verwenden)

## Zweiphasige Layout-Architektur {#two-phase-layout-architecture}

Die Phase „prepare“ (aufwendig, einmalig) wird von der Phase „layout“ (günstig, pro Größenänderung) getrennt:

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

## Intl.Segmenter für Unicode-korrekten Wortumbruch {#intlsegmenter-for-unicode-correct-word-breaking}

`Intl.Segmenter` übernimmt, was manuelles Aufteilen übersieht:

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

## Zeilenumbruchregeln nach Typ {#line-break-rules-by-type}

| Umbruchtyp | Unicode | Verhalten |
|------------|---------|-----------|
| Normaler Wortumbruch | U+0020 SPACE | Fällt mit angrenzenden Leerzeichen zusammen |
| Erhaltenes Leerzeichen | NBSP U+00A0 | Fällt nie zusammen, bricht die Zeile nur ohne Alternative |
| Zeichenloser Umbruch | U+200B ZWSP | Erlaubt einen Umbruch, rendert nichts |
| Zero-Width-Joiner | U+200D ZWJ | Verhindert einen Umbruch zwischen Zeichen |
| Weicher Trennstrich | U+00AD SHY | Fügt einen Bindestrich nur ein, wenn hier umgebrochen wird |
| Harter Umbruch | U+000A LF | Bricht immer um |
| Tabulator | U+0009 | Erweitert bis zum nächsten Tabulatorstopp |

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

## Zeilenlayout mit variabler Breite {#variable-width-line-layout}

Jede Zeile hat ihre eigene maximale Breite (Text fließt um ein Bild herum):

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

## Shrinkwrap / Ausgewogene Textbreite {#shrinkwrap-balanced-text-width}

Die optimale Containerbreite finden, um ungenutzte Zeilenbreite zu minimieren (ausgewogenes Layout):

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

## Render-Ziele {#rendering-targets}

### Canvas-Rendering {#canvas-rendering}

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

### SVG-Rendering {#svg-rendering}

```javascript
function renderSVGLines(lines: string[], x: number, y: number, lineHeight: number): string {
  return lines.map((line, i) =>
    `<text x="${x}" y="${y + i * lineHeight}" font-size="16" font-family="system-ui">${
      line.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    }</text>`
  ).join('\n');
}
```

### DOM-Rendering (mit vorberechneter Höhe) {#dom-rendering-with-pre-computed-height}

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

## CI-Pipeline: Layoutvalidierung {#ci-pipeline-layout-validation}

Prüfen, dass KI-generierte UIs Buttons nicht überlaufen und Beschriftungen nicht abschneiden, und zwar ohne Browser:

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
    ['OK', true]])('"%s" fits: %s', (label, expected) => {
    expect(validateButtonLabel(label, buttonWidth)).toBe(expected);
  });
});
```

## Unterstützung für RTL-Text {#rtl-text-support}

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

## Stolperfallen {#gotchas}

- **`measureText` benötigt geladene Schriften:** Ist die Seitenschrift noch nicht geladen, misst Canvas mit der Ersatzschrift und liefert falsche Breiten. Vor dem Aufruf von `prepare()` immer auf `document.fonts.ready` warten oder bei dynamisch geladenen Schriften `FontFace.load()` verwenden. Messungen vor dem Laden der Schrift verwenden stillschweigend falsche Metriken.
- **Die `measureText`-Breite entspricht nicht der sichtbaren Breite bei Emoji und ZWJ-Sequenzen:** Mehrcodepunkt-Emoji (z. B. das Familien-Emoji `👨‍👩‍👧`) werden in manchen Umgebungen als einzelne Glyphe gemessen, von `Intl.Segmenter` dagegen als mehrere Zeichen. Immer zuerst segmentieren und dann jedes Segment messen, nicht jeden Codepunkt.
- **CJK-`word-break: keep-all` ist nicht der Standard:** Bei Koreanisch, Chinesisch und Japanisch erlauben Browser standardmäßig Zeilenumbrüche zwischen zwei beliebigen CJK-Zeichen. In bestimmten Kontexten (`keep-all`) sollten Umbrüche nur an Leerzeichen oder Satzzeichen erfolgen. Die Layout-Engine muss dies bei Bedarf explizit umsetzen.

## Pretext-Bibliothek {#pretext-library}

`github.com/chenglou/pretext` (über 41.000 Sterne, MIT-Lizenz): Referenzimplementierung von DOM-freiem Textlayout, geschrieben vom Autor von React Motion und ReasonML. Unterstützt über 15 Sprachen, 8 Umbruchtypen, Shrinkwrap, Layout mit variabler Breite und reichen Inline-Fluss. TypeScript, Bun-Runtime.

## Siehe auch {#see-also}

- [[web-frontend/react-rendering-internals]] - React-Reconciler und Batching von DOM-Updates
- [[web-frontend/css-box-model-and-layout]] - wann DOM-Layout akzeptabel ist
- [[web-frontend/js-dom-and-events]] - Auslöser von Reflows und Batching mit `requestAnimationFrame`
