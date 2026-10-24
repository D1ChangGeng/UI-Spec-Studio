# Asset review workbench

A bounded, runnable application of the common asset method. It inherits the
repository's readable document layout and original illustration family, then uses
a sourced Lucide icon and a small authored motion fixture to exercise actual
viewing and delivery conditions. It is a QA workbench, not a new identity proposal.

```bash
python -m http.server 8080
# Open /examples/asset-review/index.html
python tools/validate_assets.py --output-dir scenario-evidence/assets
```

## Source-to-placement record

| Asset | Role / master | Delivery and adaptation | Observed target |
|---|---|---|---|
| Publication illustration | Explain source → choice → result; `tools/readme_art.py` | Four SVG outputs in `docs/assets`, selected by viewport/theme with reserved aspect ratio | Informative image and native text; source selection, fit, visual inspection and blocked-media fallback |
| Search | Familiar functional cue; exact Lucide SVG, blob `03e442a5440cff92c219fe3a3c1f2b0788d30701` | Native inline copies at 16/24/32/48 CSS px; 20px symbol in a named 44px-minimum control | Small-size rendering, currentColor, target size, keyboard operation and correct accessible meaning |
| Type specimen | Ordinary reading, mixed Latin/CJK/numerals | Installed system stack; no font redistribution or custom-font claim | Actual text, font readiness and rendered glyph inspection |
| Decorative orbit | Local motion-control test | CSS with a stable static state; pause, visibility and reduced-motion ownership | Real computed animation state, controls and preferences |

[Source notices](THIRD-PARTY.md) preserve the copied icon's licensing and identity.
The diagrams remain selectable/explainable through adjacent text even when an
image cannot load. Third-party service marks and new identity design are method
coverage, not assets created by this fixture.

## Verification conditions

The runner uses real local HTTP, Chromium and viewport sizes 390×844 and
1440×1000, in light/dark, at device pixel ratios 1 and 2. It captures the viewport,
full content and actual-size icon region. A separate blocked-artwork run checks
meaningful fallback and reserved frame geometry. Motion checks include user pause,
reduced preference and offscreen suspension. It records source identities, byte
sizes, currentSrc, geometry and environment for reproducibility.

A static metadata check supports file/record integrity; opening captures supports
visual observations. These tests exercise the stated assets and browser behavior.
They do not test custom font manufacturing, original favicon approval, professional
3D authoring or third-party animation runtimes. Those chosen production routes
require their own files, tool runs and acceptance in a real project.

The optional `--in-memory` mode embeds the same local source bytes and tests
decoding failure rather than an HTTP abort. Its result is
`offline_render_pass_http_pending`: rendering and states are observed, while
ordinary network delivery remains for the default HTTP run required by CI.
