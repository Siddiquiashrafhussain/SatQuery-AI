# SatQuery-AI — High-Contrast Dark Theme

Reference DESIGN.md for structural layout, solid dark backgrounds, stark high-contrast typography, and minimal styling. 

## 1. Visual Theme & Atmosphere

High-contrast, brutalist, and highly legible. Focused strictly on data visualization and geospatial analysis. The aesthetic rejects glassmorphism in favor of distinct, fully opaque boundaries.

Mood: utilitarian, professional, data-driven, and high-visibility.

## 2. Color Palette & Roles

```css
--bg:              #0a0a0a   /* Pure dark background */
--surface:         #171717   /* Opaque dark gray for panels */
--surface-strong:  #262626   /* Slightly lighter for active elements */
--text:            #fafafa   /* Off-white for high legibility */
--text-muted:      #a3a3a3   /* Secondary text */
--border:          #333333   /* Hard boundaries */
--border-alt:      #404040
--accent:          #10b981   /* High-contrast emerald (or amber) */
--accent-soft:     #059669
```

## 3. Typography Rules

- **Headlines:** `Space Grotesk`, fallback `Inter`. Weight 600 or 700 for distinct visual hierarchy.
- **Body:** `Inter`, weight 400 or 500, 16px. Ensure minimum 4.5:1 contrast ratio.
- **UI:** `Inter` medium or `DM Mono` for data and metrics.

## 4. Component Stylings

**Buttons**
- Primary: `--accent` fill, black text (for contrast), radius 4px to 8px, flat, no shadows.
- Secondary: `--surface-strong` fill, 1px solid `--border`, radius 4px to 8px.

**Cards & Panels**
- `--surface` fill, 1px solid `--border`, radius 8px.
- **Strictly No backdrop-filter or blur effects.**
- No inner highlights or glowing box-shadows.

**Inputs**
- `--surface` fill, 1px solid `--border-alt`, radius 6px.
- Focus: 2px solid `--accent` ring with 2px offset.

**Navigation**
- Flat, opaque header or sidebar. `--bg` or `--surface`, solid 1px border.

## 5. Layout Principles

- 1200px max, 32px gutter.
- Background is a solid color (`#0a0a0a`). No gradients.
- Corner radii are modest (4px–8px) to reinforce structural rigidity.

## 6. Depth & Elevation

Depth is achieved purely through distinct border lines and slight brightness variations in surface colors (`#0a0a0a` vs `#171717`). 
- **Do not use drop shadows** to indicate elevation.

## 7. Do's and Don'ts

**Do**
- Use fully opaque surfaces.
- Rely on border lines to separate structural elements.
- Maintain a strictly monochromatic dark base with a single high-visibility accent color.

**Don't**
- Use `backdrop-filter: blur()`.
- Use translucent background colors (e.g., `rgba(..., 0.6)`).
- Use pastel colors, soft radial gradients, or glowing effects.
- Use soft rounded corners > 12px.

## 8. Responsive Behavior

- Collapse sidebars to bottom bars on mobile.
- Retain high contrast and hard borders across all screen sizes.

## 9. Agent Prompt Guide

Bias: solid black/dark gray backgrounds (`#0a0a0a`, `#171717`), hard 1px borders (`#333`), highly legible typography, high-contrast accent colors (emerald/amber).

Reject: translucent surfaces, glassmorphism, soft shadows, pastel gradients, and rounded aesthetic.
