# Style: color-block promo

Source reference: Outwitly "UX & Service Design Agency" promo (72 s, 1080p, 23.976 fps).
What we took from it, and how it maps to code in `videos/conversion-tracking-promo`.

## What the reference does

- Real presenter and testimonial footage (we have none, so scenes are fully graphic).
- Full-bleed saturated color blocks with a huge 2 to 3 word headline on the left ("Endless Resumes", "Wasted Time").
- Floating white / translucent cards on the right, slightly rotated, stacked like paper.
- A white asterisk brand mark in a corner, rotating slowly.
- Circle wipes between scenes (a big circle grows from a corner).
- One-line captions where the spoken word gets an orange pill.
- Calendar style highlight bar sliding across items ("2 Weeks").
- Logo end card on a solid color.
- Upbeat, light music with small whooshes and pops.

## Tokens (defined once in index.html :root by build.mjs)

| Token | Value | Use |
| --- | --- | --- |
| `--magenta` | `#b4519e` | main brand block, end card |
| `--orange` | `#f4a51c` | highlight pills, caption active word, accent text |
| `--lime` | `#b6d334` | secondary block, success |
| `--plum` | `#3a1648` | dark block, code card |
| `--cream` | `#f7f1ea` | light scenes (intro, workflow) |
| `--ink` | `#2a0f35` | text on light / lime / orange |
| `--bad` | `#e23d5b` | error markers |
| `--ok` | `#1fa971` | ok markers |

Type: Montserrat. Headlines `.big` 800 weight, 118 to 150 px, letter-spacing -0.035em, line-height 0.98.
Body on cards 24 to 34 px, 600 to 800 weight. Mono: JetBrains Mono for event payloads.

## Shared classes

- `.wipe` full-frame clipped container; animate `clipPath: circle(0% at X Y)` to `circle(150% at X Y)`.
- `.fill` full-frame background layer inside a wipe.
- `.paper` white card with soft plum shadow. `.glass` translucent white card for "behind" layers.
- `.pill` rounded pill. `.ast` asterisk (3 bars, `color` sets the color). `.demo` "DEMO DATA" label.

## Scene recipe

1. Scene root `<div id="xx-wipe" class="wipe">` with a `.fill` color layer first.
2. Asterisk in a corner: scale in with `back.out`, then a slow linear rotation for the rest of the scene.
3. Headline masks: each line in `<div style="overflow:hidden"><span>`; tween `yPercent: 110 -> 0`, stagger 0.15 to 0.2.
   Give the mask `padding-bottom: 0.1em; margin-bottom: -0.1em` so descenders are not clipped.
4. Cards: `fromTo` with `x: 120+, rotation: 4 to 8` to `x: 0, rotation: -3 to 2`, `back.out(1.3 to 1.6)`.
5. In-scene beats switch color with a nested `.wipe` panel growing from a different corner each time.
6. Every visual beat starts at a cue `c[i]` (+ small offset) so it lands on the words.
7. Declare matching SFX in the scene's `SFX` list (see the skill).

## Motion timing

- Scene wipe 0.6 s, `power2.inOut`. In-scene panel wipe 0.7 s.
- Reveals 0.4 to 0.7 s. Pops 0.3 to 0.5 s with `back.out(2 to 3)`.
- Hold the end card at least 3 s.
