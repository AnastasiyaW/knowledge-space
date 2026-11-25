---
title: "Mise en page et mesure de texte sans DOM"
category: reference
tags: [web-frontend, text-layout, canvas, performance, line-breaking, reflow, pretext, virtualization, cjk]
level: 3
source_sha256: fcb534d8cf273d3a36907df5e27450524baa040880192d1583867549d8b40b26
translation: machine
translated_at: '2026-10-24'
---
# Mise en page et mesure de texte sans DOM {#dom-free-text-layout-and-measurement}

Mesurer et mettre en page du texte sans déclencher de reflow du DOM du navigateur. Essentiel pour les listes virtualisées, les moteurs de rendu canvas, le rendu côté serveur et la validation de mise en page en temps réel dans les pipelines CI.

## Le problème de la mesure via le DOM {#the-dom-measurement-problem}

La mesure du texte via le DOM du navigateur provoque un reflow de la mise en page :

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

**Impact :** dans les listes virtualisées de plus de 1 000 éléments, l'estimation de hauteur basée sur le DOM bloque le défilement. Dans les interfaces de chat, une hauteur précise calculée avant le rendu permet un défilement fluide jusqu'en bas, sans saut.

## API Canvas : mesure native du navigateur {#canvas-api-browser-native-measurement}

La seule mesure de texte sans reflow dans les navigateurs est `CanvasRenderingContext2D.measureText()` :

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

**Limitations :**
- Ne renvoie que des métriques de ligne unique, sans retour à la ligne multiligne
- Pas d'accès aux positions individuelles des glyphes
- Ne gère pas correctement les scripts complexes (mise en forme de l'arabe, découpage syllabique du thaï) sans traitement supplémentaire
- La police doit être chargée avant la mesure (utiliser `document.fonts.ready` ou `FontFace.load()`)

## Architecture de mise en page en deux phases {#two-phase-layout-architecture}

Séparer la phase « prepare » (coûteuse, exécutée une seule fois) de la phase « layout » (peu coûteuse, exécutée à chaque redimensionnement) :

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

## Intl.Segmenter pour la coupure de mots conforme à Unicode {#intlsegmenter-for-unicode-correct-word-breaking}

`Intl.Segmenter` gère ce que le découpage manuel ne prend pas en compte :

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

## Règles de coupure de ligne par type {#line-break-rules-by-type}

| Type de coupure | Unicode | Comportement |
|-----------------|---------|--------------|
| Coupure de mot normale | U+0020 SPACE | Se regroupe avec les espaces adjacents |
| Espace préservé | NBSP U+00A0 | Ne se regroupe jamais, ne coupe la ligne que s'il n'existe pas d'alternative |
| Coupure de largeur nulle | U+200B ZWSP | Autorise la coupure, n'affiche rien |
| Joiner de largeur nulle | U+200D ZWJ | Empêche la coupure entre les caractères |
| Trait d'union conditionnel | U+00AD SHY | Insère un trait d'union uniquement lorsque la coupure a lieu ici |
| Saut de ligne forcé | U+000A LF | Coupe toujours |
| Tabulation | U+0009 | Se développe jusqu'à la prochaine tabulation |

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

## Mise en page de ligne à largeur variable {#variable-width-line-layout}

Chaque ligne a sa propre largeur maximale (texte contournant une image) :

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

## Shrinkwrap / largeur de texte équilibrée {#shrinkwrap-balanced-text-width}

Trouver la largeur de conteneur optimale pour minimiser les lignes gaspillées (mise en page équilibrée) :

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

## Cibles de rendu {#rendering-targets}

### Rendu canvas {#canvas-rendering}

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

### Rendu SVG {#svg-rendering}

```javascript
function renderSVGLines(lines: string[], x: number, y: number, lineHeight: number): string {
  return lines.map((line, i) =>
    `<text x="${x}" y="${y + i * lineHeight}" font-size="16" font-family="system-ui">${
      line.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    }</text>`
  ).join('\n');
}
```

### Rendu DOM (avec hauteur pré-calculée) {#dom-rendering-with-pre-computed-height}

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

## Pipeline CI : validation de la mise en page {#ci-pipeline-layout-validation}

Tester que les interfaces générées par IA ne débordent pas des boutons et ne tronquent pas les libellés, sans navigateur :

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

## Prise en charge du texte RTL {#rtl-text-support}

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

## Pièges {#gotchas}

- **`measureText` nécessite des polices chargées** - si la police de la page n'est pas encore chargée, Canvas mesure avec la police de repli et renvoie des largeurs erronées. Toujours attendre `document.fonts.ready` avant d'appeler `prepare()`, ou utiliser `FontFace.load()` pour les polices chargées dynamiquement. Les mesures effectuées avant le chargement de la police utilisent silencieusement de mauvaises métriques
- **La largeur de `measureText` ≠ largeur visuelle pour les emojis et les séquences ZWJ** - les emojis composés de plusieurs points de code (par ex. l'emoji famille `👨‍👩‍👧`) sont mesurés comme un seul glyphe dans certains environnements, mais comme plusieurs caractères par `Intl.Segmenter`. Toujours segmenter d'abord, puis mesurer chaque segment, et non chaque point de code
- **`word-break: keep-all` pour le CJK n'est pas la valeur par défaut** - en coréen, en chinois et en japonais, les navigateurs autorisent par défaut une coupure de ligne entre deux caractères CJK quelconques. Dans certains contextes (`keep-all`), les coupures ne doivent intervenir qu'aux espaces et à la ponctuation. Votre moteur de mise en page doit l'implémenter explicitement si nécessaire

## Bibliothèque Pretext {#pretext-library}

`github.com/chenglou/pretext` (plus de 41 K étoiles, licence MIT) - implémentation de référence de la mise en page de texte sans DOM, par l'auteur de React Motion et ReasonML. Prend en charge plus de 15 langues, 8 types de coupure, shrinkwrap, mise en page à largeur variable et flux inline riche. TypeScript, runtime Bun.

## Voir aussi {#see-also}

- [[web-frontend/react-rendering-internals]] - réconciliateur React et regroupement des mises à jour du DOM
- [[web-frontend/css-box-model-and-layout]] - quand la mise en page DOM est acceptable
- [[web-frontend/js-dom-and-events]] - déclencheurs de reflow et regroupement avec `requestAnimationFrame`
