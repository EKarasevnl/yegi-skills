# Designing a deck

How to design and build a deck that mirrors the structure of its message, then prove it renders correctly. Read `style-system.md` and `voice.md` first.

The numbers in this file (word counts, block counts, sizes) are sensible defaults, not pass/fail rules. What is not negotiable is the visual system and correctness: palette, fonts, no logos, no overflow, no clipping, legible type.

## Contents
- Part 1: Designing a slide (six steps)
- The evaluation gate (mandatory)
- Variety and coherence across the deck
- Part 2: The pattern menu
- Anti-patterns

---

# Part 1: Designing a slide

Work through these before writing HTML. Skip for purely text slides (cover, single statement, close). Spend more time on slides with 5+ pieces of information.

If the result is a uniform table of label → content rows with identical weight, this step was skipped. Redo it.

## Step 1: Write the one-sentence point

What is this slide saying? One sentence. If it cannot be written, the slide is not ready. That sentence is the design brief, and usually becomes the headline.

Example: "Every investment category needs a current plan and a reason." This already says the structure: a set of categories × two attributes, plus one thing that ties them together.

## Step 2: Find the structure

Most "lists" hide a structure. Common shapes:

- **Flow**: cause → effect, inputs → process → outputs, step 1 → 2 → 3. Horizontal or vertical arrangement with arrows. The arrow must mean real sequence.
- **Centerpiece + satellites**: one main thing supported by several smaller ones. A dominant central element with smaller elements around it.
- **Comparison**: A vs B, before vs after, today vs target. Parallel columns of equal weight.
- **Hierarchy / foundation**: a base supporting layers above. Stacked, heavier at the bottom.
- **Spectrum**: items along an axis (manual → automatic, small → large).
- **Matrix**: items × attributes. A table, but with one column or row that leads.
- **Genuine list of equals**: truly parallel items. A uniform grid. **This is rare.** If a slide feels flat, the structure was probably misread.

## Step 3: Visual hierarchy matches information hierarchy

The most important element should dominate. Tools: size, color inversion (dark fill), position (center or top), border weight (2px red). Usually exactly one dominant element per slide. Equal weight everywhere is the single most common failure.

## Step 4: Sketch before coding

A 5-line ASCII sketch commits to a structure and exposes problems for free:

```
[ eyebrow ]
[ headline sentence with red words                          ]

CATEGORY     CURRENT PLAN     WHY            ┌───────────────┐
Taxes        ____ ?           ____ ?         │ THEN (dark)   │
Pension      ____ ?           ____ ?         │ One strategy  │
Savings      ____ ?           ____ ?         │ that ties it  │
                                             └───────────────┘
```

## Step 5: Canvas fit, the stage, and legibility

**Canvas.** Slides are designed in px on a fixed 1920×1080 canvas. Never let content overflow it. If it does not fit: fewer words, group items, or split into two slides.

**Scale-to-fit stage (screen safety).** All content lives inside `<div id="fit-stage">` (1920×1080). A small script scales it: `scale = min(innerWidth/1920, innerHeight/1080)`, applied as a centered `transform`, recomputed on resize. The template implements this; copy it, do not reinvent it.
- The transform makes `#fit-stage` the containing block for `position: fixed` children, so nav and slide numbers scale too.
- **Never use `vh`/`vw` inside slides.** Convert `Nvh` → `N×10.8px`, `Nvw` → `N×19.2px`.
- Keep critical content at least 24px inside the stage edge; TV overscan can crop the outer 3-5%.

**Legibility floor** (against the 1920×1080 canvas):
- Body and content text: min 26px, comfortable 28-32px.
- Card titles, item headings: min 30px.
- Meaningful mono labels and eyebrows: min 17px.
- Headlines: 40px or more.
- Presenter-only chrome (slide number, nav buttons) may be 11-14px.

Bigger text means less text. That is the point.

## Step 6: Render and look

Screenshot each slide with Playwright at 1920×1080 and look with fresh eyes. Does anything overflow? Is the important element dominant? Do arrows point the right way? Do SVG labels overlap? Does it read in the order the message flows?

---

# The evaluation gate (mandatory, after every deck)

A deck that has not been through this gate is not done. Render every slide headlessly (Playwright, 1920×1080, `device_scale_factor=2`), screenshot each, and **judge the pixels, never the code**. Checks 1 and 2 catch defects (always fix). Checks 3 and 4 are taste prompts (look critically; a deliberate break that looks great is fine).

## Check 1 · Style is right
- Background is cream `--bg`; dominant accent is `--red`. Anything reading orange or rust fails.
- Every color comes from `style-system.md`.
- **No logos, wordmarks, or brand badges anywhere.**
- Fonts are DM Sans + JetBrains Mono; mono only on labels, tags, numbers. No gradients, radius ≤ ~14px.

## Check 2 · Alignment is clean
- No text overflows or clips its box; ~20px+ padding around card text.
- Shared edges actually line up: card tops in a row, column left edges, title positions across slides. Anything 5px+ off, fix.
- No text overlaps lines or other text in any SVG.
- Nothing crashes into the nav or slide number. Consistent outer margins.
- **Vertical balance**: no large empty horizontal band. Either center the content block, or let the body grow under a fixed header. A card row stranded in the middle with the title far above fails. This is the most common failure; look for it first.
- **No shadows**: 1px borders only.
- **Screen safety**: verify programmatically at 1280×720, 1920×1080 and 3840×2160 that the `#fit-stage` bounding box sits fully inside the viewport, and spot-check the densest slide at 1280×720.
- **Legibility floor** met everywhere except presenter chrome.

## Check 3 · Not too much text, not too many boxes
- No walls of paragraphs. Card descriptions 1-2 sentences; bullets max ~2 lines.
- Around 6 content blocks per slide; 7+ equal boxes usually means the structure was misread or it is two slides.
- Something should lead the eye unless the layout is a deliberate comparison.

## Check 4 · Visually diverse and interesting
- The deck moves through different layout shapes. Three identical skeletons in a row usually means inertia.
- At least one real visual moment: a diagram, a big stat, an inverted dark slide or centerpiece.
- Each layout mirrors its message (a flow looks like a flow). If two slides could swap text without changing layout, the layouts are too generic.
- Interesting never means decorated.

## How to run it
1. Render and screenshot all slides. A contact sheet (all thumbnails in a grid) helps judge rhythm.
2. Go slide by slide against the four checks; write down every failure.
3. Fix, re-render, re-check. Repeat until clean, then present and mention the gate was run.

If the deck uses reveal builds, screenshot each slide with all reveals shown (`show(i, true)` in the template) and also check the first state of the densest slide.

---

# Variety and coherence across the deck

**Coherence comes from the fixed system.** Same cream, same red with the same meaning, same fonts, 1px borders, same margins and slide-number position on every slide.

**Variety comes from layout, scale, and rhythm**, not decoration:
- **Layout shape**: rotate through flow, centerpiece, comparison, matrix, stat, checklist, dark statement, matched to each slide's real structure.
- **Scale contrast**: a dense slide followed by a quiet one (a big stat, a one-line statement, the close).
- **Color as meaning**: an inverted dark slide for the one big idea, green where something is done. Never add a color because a slide looks plain.

Lay the thumbnails side by side. If two adjacent ones are indistinguishable in shape, change one.

---

# Part 2: The pattern menu

Starting points, not templates. Pick by structure (Step 2), then adapt. `assets/deck-template.html` contains working versions of the starred ones.

- **Cover** ★ · eyebrow, very large title with a red period or word, one-line subtitle, optional row of mono chips that preview the sections.
- **Section row** ★ · four or so numbered columns under a 2px rule, big red mono numbers. For an overview of parallel areas.
- **Three-card row** ★ · parallel concepts; one card leads with a 2px red border; tags aligned at the bottom.
- **Flow with hubs** ★ · inputs → dominant dark engine → outputs, with arrows that mean sequence.
- **Animated flow diagram** ★ · an SVG process whose nodes light up and lines draw step by step, with a feedback loop and flow dots at the end. See `animation.md` Part 2.
- **Matrix + dark side panel** · a table of items × attributes, with a dark panel for the one thing that ties them together.
- **List + open question** · numbered rows with status tags on the left, a dark panel posing the open question on the right.
- **Checklist** · large checkbox rows with a status tag each, for concrete to-dos.
- **Comparison** · two parallel columns, A vs B, before vs after.
- **Spectrum** · items placed along a labeled axis.
- **Big stat** ★ · one huge number in red with a short label and one line of context.
- **Stack** · a wide foundation with narrower layers on top.
- **Centerpiece + satellites** · a dominant central card with supporting cards around it.
- **Roadmap** · numbered items with dates and status tags.
- **Quote** · attributed quotation; quotation marks never overlap text.
- **Dark statement / close** ★ · full `--ink-fill` slide, white headline, red numbers. Good for the open questions or the one big idea at the end.

Rules for every pattern:
1. **Fill the canvas vertically**; never leave a body region floating between big empty bands.
2. **Cards never have shadows.** Write `box-shadow: none` explicitly.
3. **No em-dashes on any slide.**

---

# Anti-patterns

- **Uniform table of label → content rows** with identical weight. Find the real structure.
- **Pills inside wrapping paragraphs.** Either pills or prose in one cell, not both.
- **Edge-to-edge banners full of text.** Split or shorten.
- **Overlapping SVG text.** Render and inspect.
- **Footer or header crashing into the body.** Restructure the body.
- **One slide trying to be a document.** Seven equal cards is two slides, or one of them is the centerpiece.
- **Reaching for a pattern before thinking.** Patterns come after the structure is found.
- **Transition or divider slides that do no work.** The eyebrow handles section changes.
- **Accent line under titles, decorative bars, gradients.** Whitespace handles it.
- **Logos or brand marks** of any kind (unless the user supplies one and asks).

## When the user dumps a list of facts

Look for the structure before designing. Which fact is the centerpiece? Are some inputs to others, or results of others? Are some just metadata (a date, an owner) that belongs in an eyebrow? If they truly are parallel, a clean grid is correct. If the structure cannot be found, ask one targeted question, then design.
