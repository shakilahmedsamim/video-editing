# video-editing

Shakil's Claude + HyperFrames video editing workspace.

- **Workflow, rules and commands:** `.claude/skills/video-editor/SKILL.md` (start here, see FAST PATH)
- **One-command kit:** `kit/setup.sh`, `kit/new-video.sh <name> [promo|dark]`, `kit/make.sh videos/<name>`
- **Libraries:** `library/hooks.md`, `library/graphics.md`, `library/voice.md`
- **Style guide (color-block promo):** `docs/style-color-block-promo.md`
- **HyperFrames skills (upstream, unmodified):** `.claude/skills/hyperframes*`, `skills-lock.json`

## Videos

| Folder | Style | Export |
| --- | --- | --- |
| `videos/conversion-tracking-portfolio` | dark-tech explainer | `exports/conversion-tracking-portfolio-1080p.mp4` (2:12) |
| `videos/conversion-tracking-promo` | color-block promo + SFX | `exports/conversion-tracking-promo-1080p.mp4` (2:12) |
| `videos/asad-fiverr-gig` | talking-head edit (client footage, local only) | `exports/asad-fiverr-gig-1080p.mp4` (0:53) |

## Graphics

| Folder | Type | Export |
| --- | --- | --- |
| `infographics/installed-not-working` | LinkedIn case-study infographic, 1080x1350 (HTML source) | `installed-not-working-1080x1350.png` + `@2x` (2160x2700), light cream "screenshot proof" style |
| `infographics/tracking-burns-money` | LinkedIn post image, 1080x1350, navy flat vector (source: `build.py` -> `index.html`) | `tracking-burns-money-1080x1350.png` + `@2x` (2160x2700) |

Each video folder has its own `README.md` with the exact rebuild commands.
