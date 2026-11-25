# Building custom SVG diagrams

Custom SVGs go on workflow slides, operator slides, judge-loop slides, and any time a static SVG (rather than HTML layout) is the cleanest way to express relationships between elements. Load this reference whenever you're about to write inline `<svg>` markup with custom positioning.

The most common defect (named explicitly in the user's feedback): **text labels overlapping each other or overlapping diagram lines**. This guide is structured to prevent that.

## Contents
- Choose a viewBox first
- Define markers before using them
- Positioning text without overlap (the overlap defect)
- Lines and arrows
- Element layering
- Embedding raster images in SVG
- Render and inspect
- When not to use a custom SVG

## Choose a viewBox first

Pick the viewBox dimensions before drawing anything. The viewBox is your coordinate system; the SVG scales to whatever container CSS sets.

Common sizes used in decks:
- `viewBox="0 0 1080 560"` · full-width architecture diagram (matches the canonical asset)
- `viewBox="0 0 1100 380"` · workflow with 4-5 horizontal stages
- `viewBox="0 0 1100 340"` · queryable layer or applications-fan diagrams
- `viewBox="0 0 1000 220"` · single-row flow (model → judge → loop)

For new diagrams: choose width that matches the slide's content width (~1080-1200), and choose height to fit the actual elements with breathing room. Don't pick an arbitrary height and then try to cram content in.

## Define markers before using them

Arrow markers must be defined in `<defs>` before they're referenced. Use one definition per color you need.

```svg
<defs>
  <marker id="arr-red" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#E5242F"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
  <marker id="arr-gray" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#999"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

`refX=8 refY=5` aligns the arrow tip with the line's endpoint. `orient="auto-start-reverse"` lets you flip arrow direction with `marker-start` vs `marker-end`.

Use marker IDs prefixed with the diagram name (`op-arr`, `judge-arr`) to avoid collisions when multiple diagrams are on the same page.

## Positioning text without overlap

This is where SVGs go wrong. Text in SVG is positioned at a specific x,y point, and if two text elements share coordinates or sit on top of lines, you get overlapping, unreadable labels.

**Rules:**

- **Text inside a box** · center it using `text-anchor="middle"` with x at the box's horizontal midpoint. y should be `box-top + box-height/2 + font-size/3` (the +font-size/3 accounts for baseline alignment).
- **Text below a box** · place it at `y = box-bottom + (font-size + 6)`. Don't try to squeeze a label inside a small box; give it its own row below.
- **Text near an arrow** · offset by at least 12px perpendicular to the arrow direction. Never put text directly on top of a line.
- **Multi-line labels** · use multiple `<text>` elements, one per line, with y-positions stepped by `line-height` (typically font-size * 1.4).

**Example: a labeled box with a sub-label**

```svg
<rect x="100" y="100" width="200" height="60" rx="8" fill="#fff" stroke="#E5242F"/>
<text x="200" y="128" text-anchor="middle"
      font-size="14" font-weight="600" fill="#1F1F1F"
      font-family="DM Sans">Main label</text>
<text x="200" y="146" text-anchor="middle"
      font-size="10" fill="#999"
      font-family="JetBrains Mono">sub-label in mono</text>
```

The main label sits at y=128 (box midline 130, minus a few pixels for the upper label). The sub-label sits at y=146, 18px below. The box height is 60, so the box spans y=100 to y=160, and both labels are inside.

**Anti-pattern (causes overlap):**

```svg
<!-- Bad: two text elements at the same y, with an arrow going through -->
<text x="200" y="110" font-size="12" fill="#1F1F1F">Label A</text>
<line x1="100" y1="110" x2="300" y2="110" stroke="#999"/>
<text x="200" y="110" font-size="12" fill="#666">Label B</text>
```

This renders all three on the same horizontal line, with the line crossing through both text strings. Always offset text away from lines.

## Lines and arrows

Use `<line>` for straight segments. Use `<path>` for curves or right-angle bends.

```svg
<!-- Straight horizontal arrow -->
<line x1="200" y1="150" x2="400" y2="150" stroke="#999" stroke-width="1"
      marker-end="url(#arr-gray)"/>

<!-- Right-angle arrow (path with L commands) -->
<path d="M 200 100 L 200 200 L 400 200" fill="none" stroke="#E5242F"
      stroke-width="1.5" marker-end="url(#arr-red)"/>
```

Line weights:
- `stroke-width="0.8"` for hairline / subtle connectors
- `stroke-width="1"` for default connectors
- `stroke-width="1.5"` for emphasised connectors (the main flow)

## Element layering

SVG renders in document order: later elements paint on top of earlier ones. Standard layer order:

1. Background regions (rectangles with low-opacity fills)
2. Connector lines and arrows
3. Boxes (rectangles with white fill)
4. Text inside / around boxes
5. Annotations (small mono labels, icons)

If text appears behind a box, you wrote the text before the box. Move it after.

## Embedding raster images in SVG

For an icon or photo inside a diagram, use `<image>` with a data URL:

```svg
<image x="100" y="100" width="40" height="40"
       href="data:image/png;base64,..."/>
```

Embed the image as base64 so the deck stays a single self-contained file.

## Render and inspect

After writing an SVG, render the slide and look at it. Specifically check:

- Are any two text elements visually overlapping?
- Does any text sit on top of a line?
- Are arrows pointing to / from the right elements?
- Are box midpoints aligned (e.g., 4 cards in a row all centered on the same y)?
- Does the diagram fit inside the slide's content area without being squished?

If you find a defect, fix the positioning in SVG coordinates and re-render. Don't ship the defect.

## When NOT to use a custom SVG

A custom SVG is appropriate when:
- The diagram has multiple elements with spatial relationships (not just a list)
- You need arrows or connectors between specific elements
- The shape would be hard to express as HTML/CSS boxes

A custom SVG is overkill (use HTML/CSS instead) when:
- The layout is a grid of equal-weight cards
- It's a flow of 3-5 boxes in a row with simple arrows between them (use flex layout with `&rarr;` characters between)
- The content is text-heavy and the visual is just framing

## Animating a diagram

Get the static diagram right first, then add motion. Line drawing, node light-up and flow dots are specified in `animation.md` (Part 2). Two SVG-specific consequences: draw connectors before nodes so lines sit under cards, and draw arrowheads as separate shapes instead of `marker-end`, because a marker appears before its line has finished drawing.
