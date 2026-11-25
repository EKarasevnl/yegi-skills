# Animation

Three kinds of motion live in this skill:

1. **Motion on slides** (Part 1): a soft fade between slides and click-by-click reveal builds inside a slide. The deck stays a presentation that a person advances.
2. **Diagram animation** (Part 2): SVG diagrams whose lines draw themselves, whose nodes light up in order, and whose connectors carry a moving flow once complete.
3. **Looping animated demos** (Part 3): one 1920×1080 screen that plays a 9-12 second story on its own and loops, ready for screen recording to MP4.

Use the same palette and voice rules for both (`style-system.md`, `voice.md`).

---

# Part 1: Motion on slides

## Slide transitions

Slides cross-fade: every `.slide` is absolutely positioned, `opacity: 0`, and the active one gets `opacity: 1` with `transition: opacity .35s ease`. No slides that fly, zoom, flip, or wipe. The transition should be barely noticed.

## Reveal builds

Add `data-reveal="N"` (1, 2, 3...) to any element that should appear on the Nth press of → or space. Elements without the attribute are visible from the start.

```html
<div class="cards3">
  <div class="card" data-reveal="1">...</div>
  <div class="card" data-reveal="2">...</div>
  <div class="card lead" data-reveal="3">...</div>
</div>
```

```css
[data-reveal] {
  opacity: 0; transform: translateY(8px);
  transition: opacity .4s cubic-bezier(0.22, 1, 0.36, 1),
              transform .4s cubic-bezier(0.22, 1, 0.36, 1);
}
[data-reveal].visible { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  [data-reveal], .slide { transition: none; transform: none; }
}
```

Navigation logic (implemented in `assets/deck-template.html`):
- → / space: if the current slide has hidden reveal steps, show the next step; otherwise go to the next slide.
- ←: hide the last shown step; at step 0, go back to the previous slide **with all its steps shown** (`show(i, true)`), so stepping backwards never replays builds.
- Clicking a nav dot jumps to that slide at step 0.
- `show(i, true)` is global so the PPTX export script and screenshot checks can render each slide fully built.

## When to use reveals

- **Use** when the presenter talks through a sequence: steps of a flow, items of a list explained one by one, a payoff that should land after the setup (the dark "then" panel after the table).
- **Do not** reveal the headline or eyebrow. The slide's point is visible from the first frame.
- 1-4 steps per slide. More means the slide is doing too much.
- Group related elements under the same number so they arrive together.
- Do not put reveals on every slide. Two or three built slides in a deck is plenty.

## Other motion on slides

- **Bars that grow**: a bar chart whose bars transition `width` (or `height`) from 0 on reveal, `transition: width .55s cubic-bezier(0.22,1,0.36,1)`. Good for a result that should land.
- **Number count-up**: acceptable for one hero stat; keep it under 1 s.
- Nothing loops on a slide except the subtle flow dots of a finished diagram (Part 2). No parallax, no animated backgrounds.

## Timing reference

| Motion | Duration | Easing |
|---|---|---|
| Slide cross-fade | 300-400 ms | ease |
| Reveal fade + 8px rise | 400 ms | cubic-bezier(0.22, 1, 0.36, 1) |
| Bar grow | 550-600 ms | cubic-bezier(0.22, 1, 0.36, 1) |
| Line draw | 900 ms, starts 300 ms after its step | cubic-bezier(0.22, 1, 0.36, 1) |
| Node light-up pulse | 1.1 s | cubic-bezier(0.22, 1, 0.36, 1) |
| Arrowhead appears | 250 ms, after the line (≈1.1 s delay) | ease |
| Flow dot along a connector | 1.6 s per short line, 3 s+ per long loop | linear |
| Hover on nav buttons | 150 ms | linear |

---

# Part 2: Diagram animation

A diagram builds in the same order the presenter explains it. Every motion means something: a line drawing = "this leads to that", a node lighting up = "now we are here", flow dots = "this runs continuously". The worked example is slide 05 of `assets/deck-template.html`. Build the SVG first by the rules in `svg-building.md`, check it renders with everything visible, then add motion.

## The three effects

**1. Lines that draw themselves.** Give the path `pathLength="1"`, so the dash math works for any length, and the class `draw`:

```html
<path class="draw" data-reveal="1" pathLength="1" d="M420 225 L612 225"/>
```
```css
.draw { fill: none; stroke: var(--text); stroke-width: 3; stroke-linecap: round;
        stroke-dasharray: 1; stroke-dashoffset: 1; }
.draw[data-reveal] { opacity: 1; transform: none;          /* override the default fade */
        transition: stroke-dashoffset .9s var(--ease) .3s; } /* wait for its node first */
.draw[data-reveal].visible { stroke-dashoffset: 0; }
```

Do not use `marker-end` for arrowheads on drawn lines: the marker shows before the line finishes. Draw the arrowhead as its own `<polygon class="head">` with the same `data-reveal` step and a delay (`transition: opacity .25s ease 1.1s`) so it lands when the line arrives.

**2. Nodes that light up in order.** Each node is a `<g class="node" data-reveal="N">` with a rect and its text. It fades in with the normal reveal, and a one-off keyframe flashes its border red and its fill `--red-soft`, then settles back to the normal card look:

```css
.node.visible rect { animation: lit 1.1s var(--ease); }
@keyframes lit { 0%   { stroke: var(--red); stroke-width: 4; fill: var(--red-soft); }
                 100% { stroke: var(--border); stroke-width: 2; fill: var(--surface); } }
```

The node that is the point of the slide (`.node.lead`) keeps a 3px red border after its pulse. Only one lead node per diagram.

**3. Flow along connectors.** After the last step, small red dots travel along the connectors to show that the process keeps running:

```html
<g class="flowdots" data-reveal="4">
  <circle r="7"><animateMotion dur="1.6s" repeatCount="indefinite" path="M420 225 L612 225"/></circle>
</g>
```

Reuse the exact `d` of each connector as the `path`. Delay the group's fade-in until the last line has drawn (`.flowdots[data-reveal] { transition: opacity .3s ease 1.3s; }`), so no dot runs ahead of an unfinished line. Stagger dots with `begin="0.8s"` so they do not move in lockstep. One dot per connector, 6-8px radius, red, nothing else moves.

## Order and pacing

- One press = one stop in the story: the node and the line leading out of it arrive together, then the next press brings the next node.
- Order: node fades in and pulses (0 s) → its outgoing line draws (0.3-1.2 s) → arrowhead appears (≈1.1 s). Nothing in the same step starts at the same instant.
- Feedback loops, summary arrows, and flow dots come last, in their own step.
- 3-5 steps per diagram. More means two diagrams.

## Rules

- **Draw back-to-front in the SVG**: connectors first, nodes on top, so lines tuck under cards.
- **The finished state must pass the gate on its own.** Screenshot with `show(i, true)` and check overlap and alignment as for any static SVG. Animation never excuses a cluttered end state.
- **Flow dots only on a finished diagram**, never while it is still building, and at most one flowing diagram per deck.
- **Respect reduced motion**: lines fully drawn, no pulse, flow dots hidden.
- **No spinning, bouncing, elastic easing, or glow.**
- **Export**: `export_pptx.py` waits 1.6 s per slide so lines finish drawing. Flow dots appear as a still frame in the PPTX, wherever they happened to be; that is acceptable.

---

# Part 3: Looping animated demos

A demo is one 1920×1080 screen: a phone mockup on the left showing the product UI, a two-line headline on the right with a red payoff line, three numbered narration steps, and a small caption. It plays over 9-12 seconds and loops. It feels like a short product trailer, not a slide. Start from `assets/starter-demo.html`.

Demos use the system font stack, not Google Fonts, because they must run offline during screen recording.

## Layout

- Left region (~780px wide): the phone (380×800, 9:19.5), centered. All feature animation happens inside the phone screen.
- Right region: eyebrow (feature name, mono), two-line headline (setup line, then red payoff line), three steps (number circle + name + 1-2 sentence description), a small caption line (product name · status tag). No logo mark.
- Bottom: a scrubber (restart, play/pause, current time, progress bar, end time). It hides during recording.

## What does not go in a demo

Multiple screens, next buttons, logos, paragraphs, charts or dashboards (those belong on slides), audience names or meeting-specific content.

## The 9-second standard

- Under 9 s: too fast to read the payoff.
- 9-10 s: right for a single feature.
- 11-12 s: acceptable when the reveal needs extra time.
- Over 12 s: too long. Split or simplify. 12 s is the ceiling.

## The 3-act timeline (9 s)

| Time | Phone | Narration |
|---|---|---|
| 0.0 s | Initial state | Step 01 active, 02 and 03 pending |
| 0.0-1.5 s | Hold so the viewer reads step 01 | |
| 1.5-3.0 s | Action 01 plays (typing, tapping) | |
| 3.0 s | Action 01 done | 01 → done, 02 → active |
| 3.0-5.0 s | The mechanism (a brief "working" indicator) | |
| 5.0 s | Payoff begins | 02 → done, 03 → active |
| 5.0-7.5 s | Payoff visible (new section drops in, result appears) | |
| 7.5-9.0 s | Hold on the payoff | |
| 9.0 s | Loop | All steps reset |

## Timing principles

- **Hold before action**: 1-1.5 s after a step activates before the phone moves.
- **Hold after the payoff**: at least 2 s. It is the most important moment.
- **Step state changes are fast**: 200-300 ms.
- **Action animations are slower**: 600-1200 ms (a list appearing, a card dropping in, typing).
- **Stagger**: never start a big phone animation and a narration change on the same frame; offset by ~200 ms.
- **Sync**: step N activating must coincide with the matching phone action. Half a second off feels disconnected.
- **Do not animate the chrome**: eyebrow, headline, caption and scrubber are static from frame 1.

## Implementation

**A. JS-driven timeline (default, used by the starter).** One `requestAnimationFrame` loop computes `elapsed = ((now - start)/1000) % DURATION` and sets every state from it: step classes, scrubber position, time label, feature checkpoints. Supports pause, restart, and scrubbing, and is easy to debug.

```js
if (elapsed >= 5.0 && !dropped) { el.classList.add('visible'); dropped = true; }
if (elapsed < 0.1) { dropped = false; /* reset flags so the loop replays */ }
```

**B. CSS keyframes (only for trivial demos with no controls).** Every animation shares `animation-duration` = demo length and `animation-iteration-count: infinite`; time points are keyframe percentages (payoff at 5 s of 9 s ≈ 55%-65%).

## Export

Canvas 1920×1080, 30 fps target, MP4 at the same size. Hide the scrubber before recording.

## Honest framing

A demo shows what the product does, not proof that it works. If the feature is in a test, say so in the caption tag ("in test", "prototype"). Never put an unverified uplift number in a demo.
