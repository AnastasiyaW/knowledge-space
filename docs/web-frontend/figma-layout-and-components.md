---
title: Figma Layout and Components
category: concepts
tags: [web-frontend, figma, autolayout, components, variants, design-system]
---

# Figma Layout and Components

AutoLayout (Figma's Flexbox equivalent), constraints for positioning, and components for reusable design elements.

## AutoLayout

Makes frames behave like flex containers - children arrange, space, and resize automatically.

**Create**: Select elements -> Shift+A (or right panel "+" next to Auto Layout).

### Properties
- **Direction**: Horizontal (row), Vertical (column), Wrap
- **Gap**: space between children
- **Padding**: internal spacing (individual or uniform)
- **Alignment**: 9-point grid (top-left through bottom-right)

### Resizing Behavior

| Mode | Behavior | CSS Equivalent |
|------|----------|----------------|
| Fixed | Set size | `width: 200px` |
| Hug contents | Shrinks to fit | `width: fit-content` |
| Fill container | Expands to fill | `flex: 1` / `width: 100%` |

### Spacing Modes
- **Packed**: items cluster with defined gap (like CSS `gap`)
- **Space between**: items spread (like `justify-content: space-between`)

### Nested AutoLayout (Real Layouts)
```text
Page (vertical)
  ├── Header (horizontal)
  │     ├── Logo (fixed)
  │     ├── Nav (horizontal, gap: 24)
  │     └── CTA (fixed)
  ├── Hero (vertical, fill)
  └── Cards (horizontal, wrap)
        ├── Card 1 (vertical, fill)
        └── Card 2 (vertical, fill)
```

Mirrors HTML/CSS structure for intuitive developer handoff.

### Min/Max Constraints
Element properties -> "..." under W/H for min/max width/height. Critical for responsive behavior.

### Absolute Positioning
Toggle "Absolute position" on child to exempt from AutoLayout flow. Like `position: absolute` inside `position: relative`.

### Tips
1. Build inside-out: smallest elements first, wrap in larger AutoLayouts
2. Fill for flexible areas, Hug for natural sizing (buttons, tags)
3. 8px grid: 8, 16, 24, 32, 40, 48px spacing
4. Name frames descriptively (developers read them)

## Constraints

For fixed-position elements within non-AutoLayout frames. Controls resize behavior.

| Horizontal | Behavior |
|-----------|----------|
| Left | Fixed from left |
| Right | Fixed from right |
| Left and Right | Stretches |
| Center | Centered |
| Scale | Proportional |

Same options vertical (Top, Bottom, etc.).

**Constraints vs AutoLayout**: AutoLayout for 90% of layouts (flow-based). Constraints for edge cases (floating, overlapping).

## Components

Reusable elements. Change main component -> all instances update.

### Creating
1. Select element(s)
2. Ctrl+Alt+K -> component created (purple diamond)
3. Name with slash: `button/primary`, `button/secondary`

### Main vs Instance
- **Main** (purple diamond): source definition
- **Instance** (hollow diamond): linked copy
- Instances can override: text, fill, visibility of children
- Detach instance (right-click) to break link

## Variants

Group related component states into one component set.

### Properties
| Property | Values | Use |
|----------|--------|-----|
| State | default, hover, pressed, disabled | Interaction |
| Size | sm, md, lg | Responsive |
| Type | primary, secondary, ghost | Visual |
| Icon | true, false | With/without |

Naming: `Button/Size=md, Type=primary, State=default`

### Component Properties
- **Boolean**: show/hide child element
- **Instance swap**: replace nested component
- **Text**: expose editable text

## Design System Page

Dedicated page documenting all design decisions:
1. Color palette (swatches with hex)
2. Typography scale (all heading/body sizes)
3. Spacing scale (8px grid)
4. Component library (buttons, inputs, cards)
5. Icon set
6. Grid specs

### Styles System
```text
Color styles:  primary/500, neutral/100, accent/success
Text styles:   heading/h1, heading/h2, body/regular
Effect styles: shadow/sm, shadow/md, blur/glass
Grid styles:   reusable grid configurations
```

Slash creates folder hierarchy. Change style definition -> all instances update.

## File Organization

| Page | Content |
|------|---------|
| Cover | Project thumbnail (1920x960) |
| Design System | Styles, colors, typography, components |
| Wireframes | Low-fidelity layouts |
| Desktop | High-fidelity desktop |
| Mobile | High-fidelity mobile |
| Prototype | Connected screens |

## Gotchas

- **Constraints ignored in AutoLayout**: AutoLayout controls all child positioning
- **Variant naming**: must be exact format `Property=Value` with commas
- **Fill container only in AutoLayout**: can't use on children of non-AutoLayout frames
- **Component hierarchy**: no element of element in naming; keep flat
- **Detached instances**: lose all connection to main; can't re-attach

## See Also

- [[figma-fundamentals]] - Interface, frames, export
- [[figma-design-workflow]] - Typography, prototyping, responsive
- [[css-flexbox]] - CSS implementation of AutoLayout concepts
- [[css-responsive-design]] - Breakpoints and adaptive design
