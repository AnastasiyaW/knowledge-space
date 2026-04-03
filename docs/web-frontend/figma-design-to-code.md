---
title: Figma Design to Code
category: design
tags: [figma, design, ui-ux, design-tokens, auto-layout, components, handoff]
---

# Figma Design to Code

## Key Facts

- **Figma** is the standard design tool for web/mobile UI; browser-based, real-time collaboration
- **Auto Layout** = Figma's equivalent of CSS flexbox: direction, gap, padding, alignment, wrap
- **Components** in Figma = reusable UI elements with variants and props; map to React components
- **Design tokens** define colors, typography, spacing as reusable values; export to CSS custom properties
- **Constraints** define how elements resize relative to parent frame (pin edges, scale, fixed)
- Figma **Inspect** panel shows CSS properties: colors (hex/rgba), font properties, spacing, border-radius
- **8px grid** is the common spacing system; Figma snaps to grid by default
- **Typography scale**: define consistent sizes (12/14/16/20/24/32/48px) with matching line-heights
- Color systems: define primary, secondary, neutral, success, warning, error with shade scales (50-900)
- Dev Mode in Figma provides ready-to-use CSS, dimensions, and asset export
- Related: [[css-custom-properties-and-animations]], [[tailwind-css]], [[responsive-design-and-media-queries]]

## Patterns

### Figma Auto Layout -> CSS

```
Figma Auto Layout:                CSS equivalent:
Direction: Horizontal      ->    display: flex; flex-direction: row;
Direction: Vertical        ->    display: flex; flex-direction: column;
Gap: 16                    ->    gap: 16px;
Padding: 24                ->    padding: 24px;
Alignment: Center          ->    align-items: center;
Fill container (child)     ->    flex: 1;
Fixed width (child)        ->    flex: 0 0 auto; width: 200px;
Hug contents               ->    width: fit-content;
```

### Design Tokens to CSS Custom Properties

```css
:root {
  /* Colors from Figma color styles */
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Typography from Figma text styles */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */

  /* Spacing from Figma spacing tokens */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### Component Mapping (Figma -> React)

```
Figma Component           React Component
----------------------------------------------
Button / Primary          <Button variant="primary">
Button / Secondary        <Button variant="secondary">
Button / Disabled         <Button disabled>
Card                      <Card>
Card / With Image         <Card image={src}>
Input / Default           <Input>
Input / Error             <Input error="message">
Badge / Success           <Badge variant="success">
```

### Responsive Breakpoints from Figma Frames

```
Figma frames:                  CSS:
Mobile (375px)           ->    base styles (mobile-first)
Tablet (768px)           ->    @media (min-width: 768px)
Desktop (1440px)         ->    @media (min-width: 1024px)
```

## Gotchas

- Figma `line-height` is in pixels or percent; CSS expects unitless ratio (e.g., Figma 150% = CSS `1.5`) or px value
- Figma `letter-spacing` is in pixels or percent of font size; CSS `letter-spacing` is in `em` or `px`
- Drop shadows in Figma map to `box-shadow` in CSS; inner shadows = `box-shadow: inset ...`
- Figma fixed-width frames don't automatically translate to responsive layouts; always design with auto-layout for proper flex/grid mapping
- Figma `fill` on text/shapes maps to `color` for text and `background-color` for containers; `stroke` = `border`

## See Also

- [Figma: Dev Mode](https://www.figma.com/dev-mode/)
- [Figma: Auto Layout](https://help.figma.com/hc/en-us/articles/5731482952599-Using-auto-layout)
