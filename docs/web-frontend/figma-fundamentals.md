---
title: Figma Fundamentals
category: concepts
tags: [web-frontend, figma, design, ui-design]
---

# Figma Fundamentals

Figma is a collaborative design tool for UI/UX. Works in browser or desktop app (identical functionality). Free tier is sufficient for learning.

## Interface

- **Left panel**: layers tree (hierarchy)
- **Center**: infinite canvas
- **Right panel**: properties (dimensions, colors, effects)
- **Top toolbar**: tools (frame, shape, pen, text)

### Navigation
| Action | Shortcut |
|--------|----------|
| Zoom | Ctrl+scroll |
| Pan | Space+drag |
| Fit all | Ctrl+1 |
| Zoom 100% | Ctrl+0 |
| Zoom to selection | Shift+1 |
| Toggle grid | Ctrl+Shift+4 |

## Frames

Primary containers defining screen boundaries. Like artboards in other tools.

| Device | Width |
|--------|-------|
| Desktop | 1440px |
| Laptop | 1280px |
| Tablet | 768px |
| Mobile | 375px |

- Frames can nest (frame inside frame for sections)
- "Clip content" controls overflow visibility
- Hold Ctrl while dragging frame edges to resize without resizing children

## Grid System

Select frame -> Layout Grid -> "+" -> Columns:
- **Count**: 12 (standard for web, divides into 2/3/4/6)
- **Type**: Stretch (scales with frame)
- **Margin**: 80-120px (desktop)
- **Gutter**: 20-30px

Multiple grids can stack (columns + rows + baseline).

## Layers and Selection

- Top in panel = front on canvas (z-order)
- **Group** (Ctrl+G): visual grouping, no clip, no independent size
- **Frame** (Ctrl+Alt+G): container with clip, own dimensions, supports AutoLayout
- Click = top-level; double-click = drill in; Ctrl+click = deep select

## Shapes and Boolean Operations

Built-in: Rectangle (R), Ellipse (O), Line (L), Polygon, Star.
- Hold Shift = constrained (square/circle)
- Hold Alt = draw from center

**Boolean operations** (select 2+ shapes): Union, Subtract, Intersect, Exclude. Non-destructive by default; Flatten (Ctrl+E) makes permanent.

## Pen Tool (P)

- Click = straight anchor point
- Click+drag = curved (Bezier handles)
- Close path by clicking first point
- Double-click path to edit points

## Text

- T key, click for auto-width, click+drag for fixed-width
- Properties: font, weight, size, line-height, letter-spacing

## Export

- Select element -> Export section -> "+"
- **SVG**: icons, logos (vector, scales perfectly)
- **PNG**: graphics with transparency
- **JPG**: photographs
- Scales: 1x, 2x, 3x for retina

## Sharing

- "Share" button -> copy link
- Permissions: "can view" or "can edit"
- "Duplicate to your drafts" for editable copy

## Frames vs Groups

| Feature | Frame | Group |
|---------|-------|-------|
| Clips content | Yes | No |
| Own dimensions | Yes | No |
| AutoLayout | Yes | No |
| Fill/stroke | Yes | No |
| CSS equivalent | `<div>` | Visual grouping |

**Rule**: Frames for layout containers (map to HTML). Groups for temporary visual grouping.

## Gotchas

- **Grid is visual only**: doesn't enforce layout; elements must be positioned manually
- **Group vs Frame confusion**: use Frame when you need clipping, sizing, or AutoLayout
- **Local fonts in browser**: require Figma Font Helper plugin; desktop app loads local fonts
- **Duplicate to drafts**: original link owner controls access; always duplicate for editable work

## See Also

- [[figma-layout-and-components]] - AutoLayout, constraints, components, variants
- [[figma-design-workflow]] - Typography, color, prototyping
- [[css-grid]] - CSS implementation of Figma grid concepts
