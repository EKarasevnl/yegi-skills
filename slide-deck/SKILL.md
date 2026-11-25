---
name: slide-deck
description: Build clean, presentation-ready HTML slide decks and short animated demo screens in a warm cream-and-red editorial style, with no logos or company branding. Use when asked for slides, a deck, a presentation, a one-pager, a talk, a planning or status deck, step-by-step reveal animations on slides, animated diagrams (lines drawing, nodes lighting up, flow along arrows), or a looping animated product demo. Includes the design process, a mandatory render-and-check gate, voice rules, animation rules, a deck template, a demo starter, and a PPTX export script.
---

# Slide deck

One skill for presentation work: HTML slide decks, one-pagers, and short looping animated demos. Every output shares one visual system (cream background, near-black text, one red accent, DM Sans + JetBrains Mono) so a body of work reads as one thing.

**There is no logo and no brand mark in this system.** Do not add a company logo, wordmark, product name badge, or corner tag unless the user explicitly supplies one and asks for it. The typography and the red accent carry the identity.

## Routing: read the reference that fits the task

| The task | Read |
|---|---|
| Any deck, presentation, talk, one-pager | `references/design.md` + start from `assets/deck-template.html` |
| Slides that build step by step, slide transitions, any motion on a slide | `references/animation.md` (Part 1) |
| A diagram that animates: lines drawing, nodes lighting up in order, flow along arrows | `references/animation.md` (Part 2) + `references/svg-building.md` + slide 05 of the template |
| A looping animated demo screen (product walkthrough, feature trailer, 9-12 s) | `references/animation.md` (Part 3) + start from `assets/starter-demo.html` |
| A custom SVG diagram (architecture, flow, workflow) | `references/svg-building.md` |
| Export a finished deck to PowerPoint / Google Slides | `assets/export_pptx.py` |

**Always, for any visual or written output, also read:**
- `references/style-system.md`: palette, fonts, the no-logo rule. The single source of color truth.
- `references/voice.md`: the writing rules (no em-dashes, no buzzwords, plain English).

## The non-negotiables

1. **Red is the one accent.** `--red` `#E5242F` on cream `--bg` `#FBF9F4`. Red is a signal, never a large surface. Bold surfaces use near-black `--ink-fill` with red on top.
2. **No logos, no branding.** No logo images, no wordmarks, no "brand-tag" corners, no product badges.
3. **No overlapping text in SVGs.** Render and inspect every custom diagram (`svg-building.md`).
4. **The 1920x1080 scale-to-fit stage.** All slide content lives inside `#fit-stage`, scaled to the screen by script. Never use `vh`/`vw` inside slides. The template already does this.
5. **Legibility floor.** Body text 26px+, card titles 30px+, meaningful labels 17px+, headlines 40px+ on the 1920x1080 canvas. If it does not fit, cut words or split the slide.
6. **Every finished deck passes the evaluation gate** in `design.md`: render every slide headlessly, look at the screenshots, fix, re-render. Never ship a deck that was not rendered and looked at.
7. **No em-dashes anywhere.** Check before shipping.

## How to build (quick orientation)

1. Write the one-sentence point of each slide, find its structure (flow, centerpiece, comparison, hierarchy, spectrum, true list), sketch it in ASCII. See `design.md`.
2. Copy `assets/deck-template.html`, delete the example slides you do not need, build yours on the same CSS tokens and patterns.
3. Add `data-reveal="1"`, `"2"`, ... to elements that should appear on successive clicks (optional, see `animation.md`).
4. Render with Playwright at 1920x1080 (`device_scale_factor=2`), screenshot each slide, run the gate, fix, repeat.
5. Verify the stage fits at 1280x720, 1920x1080 and 3840x2160.
6. Optional: `python3 assets/export_pptx.py -i deck.html -o deck.pptx` for an image-per-slide PPTX (text is not editable after export).

## Files

- `references/design.md`: the six-step slide design process, the evaluation gate, deck-level variety, the pattern menu, anti-patterns.
- `references/style-system.md`: palette tokens, fonts, visual principles.
- `references/voice.md`: copy rules.
- `references/animation.md`: reveal builds and transitions on slides; diagram animation (line draw, node light-up, flow dots); timing and implementation for looping demos.
- `references/svg-building.md`: building SVG diagrams without overlap.
- `assets/deck-template.html`: a working seven-slide deck showing the stage, navigation, reveal builds, an animated SVG diagram, growing bars, and several layout patterns.
- `assets/starter-demo.html`: a 9-second looping demo with phone mockup, three narration steps, and play/pause/scrub controls.
- `assets/export_pptx.py`: HTML deck to 16:9 PPTX via headless Chromium.
