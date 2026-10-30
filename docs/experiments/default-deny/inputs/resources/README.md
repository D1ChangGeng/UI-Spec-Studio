# Common resource starting points

These are optional source leads at different scopes. A name, license or bundled
file establishes availability, not visual fitness. Inspect the exact implementation,
its original demonstration and the result under actual use in the task.

| Source | Supplied scope | Original demonstration |
|---|---|---|
| Bootstrap v5.3.8 | Album page, dashboard page, dashboard stylesheet, complete compiled CSS/JS | https://getbootstrap.com/docs/5.3/examples/album/ · https://getbootstrap.com/docs/5.3/examples/dashboard/ |
| Magic UI | MagicCard pointer surface/border and ShineBorder time-driven edge | https://magicui.design/docs/components/magic-card · https://magicui.design/docs/components/shine-border |
| Kokonut UI | CardFlip v2: reversible controlled/uncontrolled 3D card, pointer flick, keyboard input, surface light and reduced-motion handling | https://kokonutui.com/docs/cards/card-flip |

Bootstrap's original pages are Astro sources: frontmatter and its placeholder
helper require their normal site environment or a clearly labelled local rendering
adapter. The compiled CSS/JS are supplied unchanged. This is not an instruction to
install the whole Bootstrap system or mix all the listed sources.

Magic UI and Kokonut sources use React and Tailwind. The shared optional Vite
toolchain includes React, Tailwind, Motion, lucide-react and the cn utility. Read
the actual import and runtime requirements; availability does not imply adoption.
T2/T3 start as vanilla applications and may retain that runtime where appropriate.
Source translation or local rendering should preserve its source identity and
state what has actually been inspected.

Keep each adopted source's MIT notice. sources.json records pinned repository
revisions, paths and local SHA-256 identities. Existing project fixtures retain
their own authored-origin notes. The candidate pool remains open to legitimate
additional research. No stock photography or third-party raster images are bundled.
