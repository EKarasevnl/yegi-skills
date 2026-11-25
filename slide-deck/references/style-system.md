# Style system

The single source of truth for color, fonts, and visual principles. Do not redefine colors in other files or invent new ones.

## The look

Warm, confident, specific. Cream background, dark text, red as the one accent that carries meaning. Typography does most of the work. No gradients, no drop shadows, no decorative bars, no logos.

Slides should feel like a well-made technical document, not a corporate template.

## Color palette

Copy this block into the `:root` of any artifact.

```css
:root {
  /* Backgrounds */
  --bg:        #FBF9F4;   /* off-cream page background */
  --paper:     #FCF6EB;   /* warm card surface */
  --surface:   #FFFFFF;   /* white card surface: phone screens, high-contrast cards */
  --ink-fill:  #141414;   /* near-black fill for inverted / dominant cards and dark slides */

  /* Text */
  --text:      #141414;   /* primary text */
  --dim:       #54524C;   /* secondary text */
  --muted:     #A8A294;   /* tertiary text, mono labels, captions */

  /* Borders */
  --border:    #EBE4D5;   /* default card border */
  --hairline:  #E2DACA;   /* thin dividers */
  --border-sharp: #1F1F1F;/* structural borders when the grid IS the design */
  --label-bg:  #F0EAD9;   /* beige fill for mono label cells and neutral tags */

  /* PRIMARY ACCENT: RED. The one color that carries meaning. */
  --red:       #E5242F;
  --red-soft:  #FDE8EA;   /* light red wash for pills, soft callouts */
  --red-tint:  rgba(234, 29, 44, 0.06);

  /* Secondary: product chrome inside demos only, never a primary accent */
  --orange:    #E89B3F;
  --amber:     #D9A33A;

  /* Status */
  --green:     #2D7A4F;   /* live / done / positive status only */
  --warn:      #A04040;   /* watch-out and failure-mode callouts (muted, NOT the accent) */
}
```

## The dominance rule

- **Red** marks what matters: accent words in a headline, active step numbers, eyebrow squares, one emphasised card border, a key stat.
- **Red is an accent, not a surface.** No half-slide red panels, no red backgrounds behind body text. For a bold dominant surface use `--ink-fill` with red kept as the accent on top. Red should be a clear minority of the slide's area.
- **Green** only for live / done status. **`--warn`** only for genuine watch-outs. **Orange / amber** only inside demo product UI, and red must still outnumber them at least 3:1.
- Never introduce a color outside this palette.

Self-check before shipping: is the dominant accent `--red`? If it reads orange or rust, it is wrong.

## No logos

This system carries no logo, wordmark, brand badge, or corner brand tag. Do not invent one, do not render initials as a mark, do not leave an empty logo slot. If the user supplies their own logo and asks for it, place it small in one corner of the cover and close slides only, as a base64 data URL with `width: auto` so it keeps its proportions.

## Fonts

**Slides and one-pagers** use Google Fonts:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```
- DM Sans for everything readable: headlines, body, card text.
- JetBrains Mono only for labels, tags, eyebrows, numbers, step indices, status words. Usually uppercase with 0.06-0.1em letter-spacing.

**Animated demos** use the system stack (they must run offline for screen recording):
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
```

## Shared visual principles

- Cards: `border: 1px solid var(--border); box-shadow: none;` Write `box-shadow: none` explicitly. Radius 8-12px, never above ~14px.
- The dominant card is either inverted (`--ink-fill`, white text) or has a 2px red border. Only one per slide.
- Eyebrow: a 12px red square + mono uppercase label above the title. It encodes where the slide sits (section number, area name).
- Headlines are sentences that state the point, with one or two words in red.
- Tags: small mono uppercase pills. `--red-soft`/`--red` for things that need action, `--label-bg`/`--dim` for neutral status, green for done.
- Whitespace is part of the design. Leave the canvas room.
