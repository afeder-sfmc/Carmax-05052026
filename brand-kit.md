# CarMax Brand Kit

Logo source: `images/CarMax-Logo-Blue.png`

---

## Colors

### Primary Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| CarMax Navy | `#003087` | 0, 48, 135 | Logo, primary CTAs, headers, nav backgrounds |
| CarMax Dark Navy | `#002060` | 0, 32, 96 | Logo accent bars, dark backgrounds, footer |
| White | `#FFFFFF` | 255, 255, 255 | Page backgrounds, text on dark |

### Secondary / UI Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| CarMax Blue (mid) | `#0057B8` | 0, 87, 184 | Hover states, links, interactive elements |
| Light Blue | `#E6EEF8` | 230, 238, 248 | Section backgrounds, card backgrounds |
| Warm Gray | `#F5F5F5` | 245, 245, 245 | Page section alternates, form backgrounds |
| Medium Gray | `#767676` | 118, 118, 118 | Body text, secondary labels |
| Dark Gray | `#333333` | 51, 51, 51 | Primary body text |
| Border Gray | `#CCCCCC` | 204, 204, 204 | Dividers, input borders |

### Accent / Status Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Success Green | `#2E7D32` | 46, 125, 50 | Positive states, savings callouts |
| Alert Red | `#C62828` | 198, 40, 40 | Errors, warnings |
| Highlight Yellow | `#FFC107` | 255, 193, 7 | Promotional badges, attention callouts |

---

## Typography

### Font Stack
CarMax uses a clean, modern sans-serif system. Primary web font is **"CarMax Sans"** (proprietary) with fallback to system fonts.

```
font-family: "CarMax Sans", "Helvetica Neue", Arial, sans-serif;
```

For presentations and assets where CarMax Sans is unavailable, use:
- **Primary substitute**: Helvetica Neue or Arial
- **Google Fonts substitute**: Inter or Source Sans Pro

### Type Scale

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| H1 | 36–48px | 700 Bold | Hero headlines, page titles |
| H2 | 28–32px | 700 Bold | Section headers |
| H3 | 22–24px | 600 SemiBold | Card titles, subsections |
| H4 | 18–20px | 600 SemiBold | Labels, callout headers |
| Body Large | 18px | 400 Regular | Lead paragraphs |
| Body | 16px | 400 Regular | Standard body copy |
| Body Small | 14px | 400 Regular | Captions, footnotes, legal |
| Label | 12px | 600 SemiBold | Tags, badges, overlines (ALL CAPS) |

### Text Colors
- **On white/light backgrounds**: `#333333`
- **On navy/dark backgrounds**: `#FFFFFF`
- **Links**: `#0057B8` (underline on hover)
- **Muted/secondary text**: `#767676`

---

## Logo Usage

### Available Asset
- `images/CarMax-Logo-Blue.png` — full wordmark in CarMax Navy (`#003087`) on white/transparent background; includes four square accent bars beneath the wordmark

### Placement Rules
- Minimum clear space: equal to the height of the "C" in the wordmark on all sides
- On dark navy backgrounds: use white version (not available in assets — reproduce as white `#FFFFFF` wordmark)
- On white or light backgrounds: use navy version (the file provided)
- Do not recolor, stretch, or add effects to the logo

---

## Spacing & Layout

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Inline gaps, tight labels |
| sm | 8px | Component internal padding |
| md | 16px | Standard padding, card gaps |
| lg | 24px | Section padding |
| xl | 32px | Block spacing |
| 2xl | 48px | Major section breaks |
| 3xl | 64px | Hero / full-bleed section padding |

### Grid
- Max content width: **1280px**
- Column gutter: **24px**
- Mobile breakpoint: **768px**
- Card border radius: **8px**
- Button border radius: **4px** (CarMax uses fairly rectangular buttons)

---

## Component Styles

### Buttons

**Primary CTA**
```css
background: #003087;
color: #FFFFFF;
font-weight: 700;
font-size: 16px;
padding: 12px 24px;
border-radius: 4px;
text-transform: none;
```

**Secondary / Outline**
```css
background: transparent;
color: #003087;
border: 2px solid #003087;
font-weight: 700;
font-size: 16px;
padding: 12px 24px;
border-radius: 4px;
```

**Hover state**: Primary darkens to `#002060`; Secondary fills with `#003087` / white text.

### Cards
```css
background: #FFFFFF;
border: 1px solid #CCCCCC;
border-radius: 8px;
padding: 24px;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
```

---

## Asset-Type Guidelines

### Web Pages
- White body background (`#FFFFFF`)
- Navy top nav with white text/logo
- Section alternation: white ↔ `#F5F5F5` or `#E6EEF8`
- CTAs always in Navy primary button style

### Emails
- Max width: **600px**
- Header: Navy (`#003087`) background, white logo
- Body: White background, `#333333` body text
- Footer: `#F5F5F5` background, `#767676` text, legal in 12px
- Single-column for mobile safety

### Presentations (PowerPoint / Google Slides)
- Title slides: Navy (`#003087`) full-bleed background, white text, white logo
- Content slides: White background, navy H2 headers, dark gray body
- Accent color for data callouts: `#0057B8` or Highlight Yellow `#FFC107`
- Avoid heavy gradients — CarMax is flat/clean

### Data Visualizations
- **Primary series**: `#003087` (Navy)
- **Secondary series**: `#0057B8` (Mid Blue)
- **Tertiary series**: `#E6EEF8` (Light Blue)
- **Highlight / accent bar**: `#FFC107` (Yellow) — use sparingly for one key data point
- **Positive delta**: `#2E7D32` (Green)
- **Negative delta**: `#C62828` (Red)
- Chart background: White; gridlines in `#CCCCCC` at 50% opacity
- Axis labels: 12px, `#767676`

### Demo Plans / Documents
- Header stripe: Navy (`#003087`)
- Section dividers: `#E6EEF8` fill rows or `#003087` left border accent
- Tables: alternating white / `#F5F5F5` rows, navy header row with white text
- Callout boxes: `#E6EEF8` background, `#003087` left border (4px)

---

## Quick-Reference Swatches (CSS)

```css
:root {
  --carmax-navy:       #003087;
  --carmax-dark-navy:  #002060;
  --carmax-blue:       #0057B8;
  --carmax-light-blue: #E6EEF8;
  --carmax-white:      #FFFFFF;
  --carmax-gray-dark:  #333333;
  --carmax-gray-mid:   #767676;
  --carmax-gray-light: #F5F5F5;
  --carmax-border:     #CCCCCC;
  --carmax-green:      #2E7D32;
  --carmax-red:        #C62828;
  --carmax-yellow:     #FFC107;
}
```
