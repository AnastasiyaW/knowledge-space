---
title: Figma Design Workflow
category: concepts
tags: [web-frontend, figma, typography, color, prototyping, responsive]
---

# Figma Design Workflow

Typography, color theory, effects, prototyping, and responsive design workflow in Figma.

## Typography

### Font Classification
- **Serif** (Times, Playfair): classic, formal - headings in luxury/editorial
- **Sans-serif** (Roboto, Inter, Open Sans): clean, modern - default for web body
- **Monospace** (Fira Code): code blocks only
- **Display/Script**: headlines or accents only, never body text

### Typography Scale

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 48-64px | Bold 700 | 110-120% |
| H2 | 36-48px | Bold 700 | 120-130% |
| H3 | 24-32px | SemiBold 600 | 120-130% |
| Body | 16-18px | Regular 400 | 150-160% |
| Caption | 12-14px | Regular 400 | 140-150% |
| Button | 14-16px | Medium 500 | 100% |

### Rules
- Max 2 font families per project
- 45-75 characters per line for readability
- Minimum 14px on web, recommend 16px body
- All-caps: only short labels, increase letter-spacing 2-5%

## 8px Spacing Grid

All spacing multiples of 8: 8, 16, 24, 32, 40, 48, 64, 80px. 4px sub-grid for fine adjustments.

| Context | Typical Values |
|---------|---------------|
| Page margins (mobile) | 16-24px |
| Page margins (desktop) | 80-120px |
| Section padding | 64-120px |
| Card padding | 16-32px |
| Gap between cards | 16-32px |
| Button padding | 12-16px vertical, 24-32px horizontal |

## Color

### HSB Model
- **H** (Hue): 0-360 color wheel
- **S** (Saturation): 0-100% (gray to vivid)
- **B** (Brightness): 0-100% (black to full)

### Building a Palette
1. **Primary**: brand color (CTAs, links)
2. **Secondary**: complementary
3. **Neutrals**: 5-7 gray shades
4. **Semantic**: success/error/warning/info

### 60-30-10 Rule
- 60% dominant (usually neutral/white)
- 30% secondary (sections, cards)
- 10% accent (CTAs, highlights)

### Contrast
Minimum 4.5:1 for body text, 3:1 for large text (WCAG AA). Use Stark/Contrast plugins to verify.

## Effects

### Drop Shadow
Common: `X:0 Y:4 Blur:12 Color:#000 at 10-15%`. Multiple shadows can stack.

### Background Blur (Glassmorphism)
Background blur 10-20px + fill #FFF at 30-60% opacity.

### Blend Modes
Multiply (darken), Screen (lighten), Overlay (contrast). Use for image toning.

### Masks
Place shape above image -> select both -> "Use as mask" (Ctrl+Alt+M). Shape defines visible area.

## Prototyping

### Connections
1. Select trigger element (button, card)
2. Drag blue circle to target frame
3. Configure: trigger, action, animation, duration, easing

### Transition Types
- **Instant**: no animation
- **Dissolve**: cross-fade
- **Smart Animate**: interpolates matching layers (same name required)
- **Move/Push/Slide**: directional transitions

### Smart Animate
1. Create Frame A (start state)
2. Duplicate -> modify in Frame B (position, size, color, opacity)
3. Connect A->B with Smart Animate
4. Layers MUST have identical names to match

Interpolates: position, size, rotation, opacity, fill, corner radius, stroke.

### Overlays
Connect trigger -> "Open overlay" -> select overlay frame. Configure position, background dimming, close-on-click.

### Interactive Components
Define interactions WITHIN component variants (hover, press). Every instance inherits automatically.

### Duration Guidelines
| Animation | Duration |
|-----------|----------|
| Button state | 100-200ms |
| Tooltip | 150-200ms |
| Modal | 200-300ms |
| Page transition | 300-500ms |

### Easing
- **Ease out**: elements entering (most common)
- **Ease in**: elements exiting
- **Ease in-out**: elements moving within view
- Material Design: `cubic-bezier(0.4, 0.0, 0.2, 1.0)`

## Responsive Design Workflow

### Breakpoints
Design at least 3 sizes: Mobile (375px), Tablet (768px), Desktop (1440px).

### Adaptation Patterns
1. **Reflow**: horizontal -> vertical stack
2. **Hide**: remove non-essential on small screens
3. **Resize**: reduce fonts, padding proportionally
4. **Replace**: hamburger replaces horizontal nav

### Process
1. Desktop first (more space to plan layout)
2. Duplicate -> resize to tablet -> adjust
3. Duplicate -> resize to mobile -> adjust
4. Keep components consistent across breakpoints

### Export for Retina
- 1x (standard), 2x (retina), 3x (iPhone Plus/Max)
- SVG doesn't need multiple exports (vector)

## Design Principles

- **Whitespace**: more = premium feel; less = information-dense
- **Proximity**: related items close, unrelated far
- **Repetition**: consistent styles for same-level elements
- **Contrast**: size, weight, color, space differences create hierarchy
- **Alignment**: shared axes create order

## Wireframes

Low-fidelity structure planning: grayscale, simple rectangles, basic text. Test with stakeholders before investing in high-fidelity.

## Essential Plugins

| Plugin | Purpose |
|--------|---------|
| Iconify | 100k+ icons |
| Unsplash | Stock photos |
| Contrast/Stark | Accessibility checking |
| Content Reel | Placeholder data |

## Gotchas

- **Smart Animate name mismatch**: layers with different names cross-fade instead of interpolating
- **Overlay without close**: users get stuck; always enable close-on-outside-click
- **Too many fonts**: more than 2 families creates visual chaos
- **Ignoring contrast**: beautiful but unreadable text fails accessibility
- **Static mockup thinking**: not testing resize behavior early leads to non-responsive designs

## See Also

- [[figma-fundamentals]] - Interface, frames, export
- [[figma-layout-and-components]] - AutoLayout, components, variants
- [[css-animation-and-transforms]] - Implementing designed animations
- [[css-responsive-design]] - CSS media queries for breakpoints
