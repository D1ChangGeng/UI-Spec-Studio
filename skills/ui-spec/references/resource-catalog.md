# UI resource map

Find a useful starting point by need, then read the exact item and its current primary source.
Apply [the common sourcing method](component-sourcing.md) throughout selection and integration.

Research snapshot: **2026-10-24** · Catalog updated: **2026-11-18** · **80 resources** · **7 access mechanisms**.
Curated from the accepted 2026-10-24 documentation/public-source research and expanded on 2026-11-18 with high-craft registries, specialist engines, typography, icon and design-reference entries. Original observation dates are preserved per entry; all entries require current item, demo and project verification.

## Use the map

Read the relevant section, use the [structured catalog](../assets/resource-catalog.json), or query the optional local helper:

```bash
python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
python <skill-dir>/scripts/find_resources.py --list-filters
```

Queries match all supplied terms; ASCII alphanumeric terms match at token boundaries while CJK and punctuated terms match as substrings. Filters combine, and results are alphabetical discovery leads with `total_matches` and `truncated` counts. A concrete code-stack filter includes framework-neutral, multi-framework and multi-runtime candidates while excluding mismatched concrete stacks; reference and design-tool stacks stay exact. Check exact adapter compatibility in primary documentation. A missing match invites wider research. The helper reads local data and performs no installation or network operation.

Platform documentation, item inspection and project acceptance have different scopes. Review dates identify the source research, and use-time checks establish current fit. Keep actual adoption records in the project. Maintain shared entries through authorized review and normal version control.

## Needs and delivery forms

| Need | Scope |
|---|---|
| `foundations` | Tokens, theme roles, scales and spacing |
| `layout` | Page structure, navigation, blocks and responsive composition |
| `controls` | Forms, menus, overlays, focus and feedback |
| `visual-effects` | Backgrounds, surfaces, shaders and expressive treatments |
| `typography` | Fonts, reading roles, glyph coverage and text treatment |
| `icons` | Icon semantics, shapes and distribution |
| `imagery` | Photography, illustration and editable graphics |
| `motion` | Transitions, gestures, timelines and micro-interactions |
| `complex-information` | Tables, charts, editors and data relationships |
| `design-reference` | Patterns, flows and editable design sources |

Source components, packages, primitives, tokens, assets, fonts, blocks, engines, generators, design files and references each have distinct ownership and update requirements. Resources can serve several needs.

## Discover resolved visual work

Descriptive discovery routes, not a quality ranking, completeness score, closed supplier list or project adoption record.

**Shared craft-profile observation boundary:** Every `craft_profile` in this catalog is **Not rated — inspect actual demo and current-project result; public documentation/source structure, not a visual audit** or runtime endorsement. Each resource card below retains its own observation dates and primary source URLs.

**Reuse Scope** and **Visual Completeness** are independent. The former locates useful responsibility; the latter requires observing the exact item. A broad primitive library does not settle visual craft, and a resolved small effect does not settle a complete page.

Search complete pages and functional blocks when composition is the need; search visual components and assets when their material or motion supplies the defining relationship. Discover usable external mature work first and assess validated project work alongside it; select by observed quality, fit and continuity. Routine matching-condition inheritance can reuse that foundation. Original construction remains outside normal candidates under the default-deny policy in [component-sourcing.md](component-sourcing.md#default-deny-original-ui-construction).

| Source role | Responsibility to inspect | Boundary |
|---|---|---|
| Resolved page or design system | Composition, space, visual language and coordinated components | Broad scope does not guarantee high visual completeness |
| Resolved functional block | Cohesive layout, visual and interaction relationships | Trial the complete relation before splitting it |
| Resolved visual component, effect or asset | Local material, motion, imagery and states | Inspect surrounding product coherence separately |
| Functional component or interaction primitive | Semantics, focus, keyboard, state and necessary mechanics | An import does not provide unrelated visible design |
| Drawing, styling or motion technology | Operation and adaptation of selected mature work | Technical capability does not authorize original visual construction |

These roles describe actual responsibilities rather than a fixed packaging or quality rank. A source may occupy several roles. A shared system can cover many visible elements; the catalog requires neither per-element searches nor a resource-count quota. Judge acquisition, adoption and retained craft separately in the actual product.

```bash
python <skill-dir>/scripts/find_resources.py --form visual-component --stack vue --json
python <skill-dir>/scripts/find_resources.py --form blocks --stack react --json
python <skill-dir>/scripts/find_resources.py --id react-bits --json
python <skill-dir>/scripts/find_resources.py --role visual-implementation --reuse-scope block --json
```

Role/scope filters match the existing craft_profile labels literally. Unclassified leads remain available to other queries; missing profile labels do not establish unavailable resources or inferior quality. The visual-component filter identifies documented delivery form, not inspected quality. Read the original demo, exact source/configuration and use-time terms; continue outside this catalog when worthwhile. The installed inspector does not score or approve any choice.

| Resource | Documented role | Potential reuse scope | Visual search forms |
|---|---|---|---|
| 21st.dev | discovery-and-reference | page, block, component | author-specific-compositions |
| Aceternity UI | visual-implementation | visual-component, block | spotlight, cards, scroll-effects, typography |
| Animate UI | visual-implementation | visual-component, component, effect | animated-controls, state-transitions, registry-motion-components |
| Ant Design | functional-foundation, visual-implementation | component-family, tokens | enterprise-system, dense-forms, data-tables |
| Apache ECharts | functional-foundation, visual-implementation | visual-component, imagery | canvas-and-svg-charts, interactive-data-visualization |
| Ark UI | functional-foundation | primitive, component-family | state-machine-headless-primitives-visual-treatment-selected-in-context |
| assistant-ui | functional-foundation, visual-implementation | primitive, block, component-family | composable-chat-threads, tool-call-and-composer-blocks |
| Awwwards | design-reference, discovery-and-reference | page, effect, typography | art-directed-websites, expressive-motion-and-editorial-craft |
| Base UI | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| cmdk | functional-foundation | primitive, interaction-mechanism | composable-command-palette-visual-chrome-selected-in-context |
| Codrops | design-reference, discovery-and-reference | effect, visual-component, page | creative-web-demos, webgl-and-css-motion-studies |
| coss ui | functional-foundation, visual-implementation | component, block, component-family, visual-component | base-ui-particles, coordinated-controls, product-blocks |
| Cult UI | visual-implementation | visual-component, block, effect | tactile-cards, expandable-blocks, motion-compositions |
| Design Spells | design-reference, discovery-and-reference | effect, interaction-mechanism, component | micro-interaction-clips, state-transition-craft-details |
| Embla Carousel | functional-foundation, implementation-route | interaction-mechanism, effect | physics-carousel-track, drag-slide-motion |
| fffuel | visual-implementation, implementation-route | imagery, effect | svg-grain-textures, mesh-gradients, geometric-patterns |
| Finesse UI | design-reference | page, component-family | design-file-not-runtime-implementation |
| Floating UI | functional-foundation, implementation-route | interaction-mechanism | floating-positioning-and-collision-engine |
| Fonts In Use | design-reference, discovery-and-reference | typography, page | real-world-type-specimens, typographic-pairings |
| Fontshare | visual-implementation, discovery-and-reference | typography | editorial-display-typefaces, neo-grotesque-families, variable-fonts |
| Fontsource | implementation-route, visual-implementation | typography | self-hosted-fonts, variable-typefaces |
| Fumadocs | functional-foundation, visual-implementation | page, block, component-family, typography | editorial-documentation-shell, sidebar-toc-search-system |
| Godly | design-reference, discovery-and-reference | page, block, effect | high-craft-websites, section-level-ui-compositions |
| GSAP | implementation-route | effect, timeline | sequencing-engine |
| Iconify | discovery-and-reference, implementation-route | icons | multi-collection-icon-directory, svg-delivery |
| Inspira UI | visual-implementation | visual-component, effect | background, text-motion, cards, visual-interaction |
| Kokonut UI | visual-implementation | visual-component, block, effect | interactive-cards, motion-blocks, tactile-controls |
| Lenis | implementation-route | interaction-mechanism, effect | smooth-scroll-interpolation |
| LottieFiles | discovery-and-reference, implementation-route | effect, imagery | authored-vector-animation, loaders, feedback-graphics |
| Lucide | visual-implementation | icons | line-icon-family, svg-symbols |
| lucide-animated | visual-implementation | icons, visual-component, effect | motion-animated-svg-icons, hover-and-state-icon-feedback |
| Magic UI | visual-implementation | visual-component, block | border-light, text-motion, background, display-composition |
| Mantine | functional-foundation, visual-implementation | component-family, block, tokens | coordinated-react-system, prebuilt-responsive-blocks |
| Mobbin | design-reference, discovery-and-reference | page, block | shipped-product-screens, multi-step-user-flows |
| Motion | implementation-route | effect, interaction-mechanism | animation-and-input-engine |
| Motion Primitives | visual-implementation, implementation-route | visual-component, effect, interaction-mechanism | text-motion, border-effects, spring-micro-interactions |
| MUI | functional-foundation, visual-implementation | component-family, tokens | material-system, dense-controls, data-views |
| NumberFlow | visual-implementation, implementation-route | visual-component, effect, typography | rolling-numeric-transitions, tabular-kpi-motion |
| Nuxt UI | functional-foundation, visual-implementation | component-family, block, tokens | coordinated-controls, themed-system, product-layouts |
| Observable Plot | visual-implementation, implementation-route | visual-component, imagery | editorial-svg-charts, faceted-statistical-graphics |
| Open Props | visual-implementation | tokens | css-custom-properties, spacing-color-easing-scales |
| Paper Shaders | visual-implementation | effect, visual-component | shader-surface, procedural-texture, background |
| Penpot | design-reference, implementation-route | page, tokens, component-family | editable-design-files, design-tokens-mapping |
| Phosphor Icons | visual-implementation | icons | six-weight-icon-family, duotone-and-fill-icons |
| Poly Haven | visual-implementation | imagery, scene | cc0-hdri-lighting, pbr-material-textures, 3d-models |
| prompt-kit | visual-implementation | block, component | ai-prompt-composers, chat-message-blocks, streaming-response-ui |
| Radix Colors | visual-implementation | tokens | perceptual-color-scales, light-dark-surface-ramps |
| Radix Primitives | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| React Aria | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| React Bits | visual-implementation | visual-component, effect | background, text-motion, card-material, pointer-response |
| React Three Fiber & Drei | implementation-route | scene, effect | declarative-webgl-scenes, 3d-lighting-and-materials |
| Recharts | functional-foundation, implementation-route | visual-component, imagery | composable-svg-charts, responsive-data-series |
| Refero | design-reference, discovery-and-reference | page, block | shipped-web-product-screens, multi-screen-user-flows |
| Reka UI | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| Rive | implementation-route, visual-implementation | effect, interaction-mechanism, scene | state-machine-animation, interactive-vector |
| shadcn-svelte | functional-foundation, visual-implementation | component, block | coordinated-controls, svelte-product-blocks |
| shadcn-vue | functional-foundation, visual-implementation | component, block | coordinated-controls, product-blocks |
| shadcn/ui | functional-foundation, visual-implementation | component, block | coordinated-controls, product-blocks |
| SiteInspire | design-reference, discovery-and-reference | page, block | editorial-and-minimalist-websites, grid-and-pacing-references |
| SmoothUI | visual-implementation | visual-component, component, effect | micro-interactions, animated-controls, spring-transitions |
| Sonner | functional-foundation, visual-implementation | visual-component, component, interaction-mechanism | stacked-toast-notifications, gesture-dismiss-feedback |
| Spline | design-reference, visual-implementation, implementation-route | scene, imagery, effect | authored-3d-scenes, static-video-or-webgl-exports |
| Tabler Icons | visual-implementation | icons | customizable-stroke-svg-icons, filled-and-outline-glyphs |
| Tailark | visual-implementation | block, page | marketing-sections, hero-compositions, pricing-and-feature-grids |
| TanStack Table | functional-foundation | interaction-mechanism | headless-table-state-visual-treatment-selected-separately |
| The Component Gallery | design-reference, discovery-and-reference | component-family, component, tokens | cross-system-component-taxonomy, live-design-system-directory |
| Tiptap | functional-foundation, implementation-route | component, interaction-mechanism | headless-rich-text-editor-visual-chrome-selected-separately |
| tldraw | functional-foundation, visual-implementation, implementation-route | page, scene, interaction-mechanism | infinite-spatial-whiteboard, vector-drawing-canvas |
| Tremor | visual-implementation | block, visual-component, component-family | kpi-cards, analytics-dashboard-blocks, data-charts |
| tweakcn | visual-implementation, discovery-and-reference | tokens | oklch-color-themes, semantic-token-presets, surface-elevation-ramps |
| Typewolf | design-reference, discovery-and-reference | typography, page | curated-web-font-pairings, live-site-type-specimens |
| Uiverse | discovery-and-reference, visual-implementation | component, visual-component, effect | community-controls, loaders, cards, css-effects |
| unDraw | visual-implementation | imagery | recolorable-flat-svg-illustrations |
| Unicorn Studio | visual-implementation, implementation-route | scene, effect, imagery | interactive-webgl-backgrounds, layered-shader-scenes |
| Unsplash | visual-implementation, discovery-and-reference | imagery | editorial-photography, subject-imagery |
| Utopia | design-reference, implementation-route | tokens, typography | fluid-type-scales, fluid-space-and-grid |
| Vaul | functional-foundation, implementation-route | primitive, interaction-mechanism | touch-physics-drawer, bottom-sheet-snap-points |
| Vue Bits | visual-implementation | visual-component, effect | background, text-motion, cards, interaction |
| Web Awesome | functional-foundation, visual-implementation | component-family, tokens | web-components-design-system, custom-element-controls |
| xyflow / React Flow | functional-foundation, implementation-route | component, interaction-mechanism, scene | node-edge-canvas, pan-zoom-workflow-graphs |

Finesse UI (finesseui.com) is a design-kit entry. The separately studied mouse-lin/finesse-skill is a method source, not that kit or a bundled runtime implementation.

## Resource cards

### 21st.dev (`21st`)

Community component, block, theme and template discovery.

**Find by:** layout, visual-effects. **Form:** source, blocks, reference. **Stack scope:** react.
**Access:** Search/catalog, previews and item-specific installation or prompt export.
**Adoption judgment:** Resolve original author/source, access terms and source completeness before adoption.
**Primary sources:** [Source 1](https://21st.dev/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: discovery-and-reference; potential scope: page, block, component; forms: author-specific-compositions.

### Aceternity UI (`aceternity`)

Backgrounds, cards, scroll effects, text and showcase compositions.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Visual catalog, demos, usage code and component docs.
**Adoption judgment:** Review exact source, rights, dependencies and touch behavior; adapt strong effects to the accepted visual direction.
**Primary sources:** [Source 1](https://ui.aceternity.com/components)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: visual-implementation; potential scope: visual-component, block; forms: spotlight, cards, scroll-effects, typography. **Profile sources:** [Source 1](https://ui.aceternity.com/components/spotlight-new)

### Animate UI (`animate-ui`)

Animated React, Tailwind CSS and Motion component distribution covering primitives, controls and visual effects.

**Find by:** motion, controls, visual-effects. **Form:** source, registry, visual-component. **Stack scope:** react.
**Access:** Documentation, live demos, registry CLI installation and editable component source.
**Adoption judgment:** Check primitive dependencies, animation timing defaults and reduced-motion fallbacks; avoid mixing multiple incompatible motion engines in one surface.
**Primary sources:** [Source 1](https://animate-ui.com/docs)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: visual-component, component, effect; forms: animated-controls, state-transitions, registry-motion-components.

### Ant Design (`ant-design`)

Data-dense forms, tables, navigation and feedback.

**Find by:** controls, complex-information, layout. **Form:** package, system. **Stack scope:** react.
**Access:** Bilingual AI docs, component Markdown, semantic structure, design docs and MCP links.
**Adoption judgment:** Inspect component semantics and version; other framework implementations have their own contracts.
**Primary sources:** [Source 1](https://ant.design/docs/react/llms/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component-family, tokens; forms: enterprise-system, dense-forms, data-tables.

### Apache ECharts (`echarts`)

Charts, visual relationships, interaction and server-rendered graphics.

**Find by:** complex-information, imagery. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** Example editor with code export, APIs and handbook.
**Adoption judgment:** Choose the right representation and renderer; test real data and accessible equivalents.
**Primary sources:** [Source 1](https://echarts.apache.org/handbook/en/basics/import/) · [Source 2](https://echarts.apache.org/handbook/en/best-practices/canvas-vs-svg/) · [Source 3](https://echarts.apache.org/handbook/en/how-to/cross-platform/server/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: visual-component, imagery; forms: canvas-and-svg-charts, interactive-data-visualization.

### Ark UI (`ark-ui`)

Zag.js state-machine headless accessible UI primitives for React, Vue, Svelte and Solid.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** react, vue, svelte, solid, multi-framework.
**Access:** Multi-framework documentation, package APIs and open-source GitHub repository.
**Adoption judgment:** Pair headless state-machine behavior with a deliberately selected visual system and tokens; verify framework-specific styling hooks and keyboard/ARIA attributes in the assembled page.
**Primary sources:** [Source 1](https://ark-ui.com/) · [Source 2](https://github.com/chakra-ui/ark)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation; potential scope: primitive, component-family; forms: state-machine-headless-primitives-visual-treatment-selected-in-context.

### assistant-ui (`assistant-ui`)

Composable AI chat and thread UI primitives, streaming runtime adapters and turnkey conversation blocks.

**Find by:** controls, layout, complex-information. **Form:** package, primitive, blocks. **Stack scope:** react.
**Access:** Packages, primitive APIs, starter blocks and open-source GitHub repository.
**Adoption judgment:** Separate primitive thread state from visual surface styling; verify accessibility, streaming auto-scroll interruption and tool-call rendering under real latency and failures.
**Primary sources:** [Source 1](https://github.com/assistant-ui/assistant-ui)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: primitive, block, component-family; forms: composable-chat-threads, tool-call-and-composer-blocks.

### Awwwards (`awwwards`)

Art-directed web craft, expressive typography, layout pacing and interaction award showcase.

**Find by:** design-reference, visual-effects, motion. **Form:** reference. **Stack scope:** reference.
**Access:** Public award directory, element collections and live links to original published sites.
**Adoption judgment:** Follow through to the live published site to inspect real responsiveness, motion restraint and readability; treat showcase art direction as expressive calibration while verifying product usability independently.
**Primary sources:** [Source 1](https://www.awwwards.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: page, effect, typography; forms: art-directed-websites, expressive-motion-and-editorial-craft.

### Base UI (`base-ui`)

Customizable menus, overlays and form interaction foundations.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** react.
**Access:** llms index, APIs/examples and package installation.
**Adoption judgment:** Check controlled state, portals, focus and styling scope; validate accessibility in the composed result.
**Primary sources:** [Source 1](https://base-ui.com/react/overview/quick-start) · [Source 2](https://base-ui.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.

### cmdk (`cmdk`)

Fast, composable command palette and searchable menu primitive with keyboard navigation.

**Find by:** controls, complex-information. **Form:** package, primitive. **Stack scope:** react.
**Access:** Package installation, API examples and open-source GitHub repository.
**Adoption judgment:** Pair with a deliberately sourced dialog surface and semantic tokens; verify async filtering, empty states, IME composition for CJK input and screen-reader announcements.
**Primary sources:** [Source 1](https://github.com/dip/cmdk)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation; potential scope: primitive, interaction-mechanism; forms: composable-command-palette-visual-chrome-selected-in-context.

### Codrops (`codrops`)

Creative composition, graphics, interaction and implementation techniques.

**Find by:** design-reference, visual-effects, motion. **Form:** reference, source. **Stack scope:** reference.
**Access:** Search/categories, live demonstrations and tutorial/source pairs.
**Adoption judgment:** Extract transferable mechanisms and assess each example license, dependencies and product fit.
**Primary sources:** [Source 1](https://tympanus.net/codrops/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: effect, visual-component, page; forms: creative-web-demos, webgl-and-css-motion-studies.

### coss ui (`coss-ui`)

Base UI and Tailwind CSS component particles and blocks (successor to Origin UI) with accessible state wiring.

**Find by:** controls, layout. **Form:** source, blocks, registry, visual-component. **Stack scope:** react.
**Access:** Component/particle catalog, live previews, shadcn-compatible registry CLI and public GitHub source.
**Adoption judgment:** Confirm Base UI vs Radix API contracts when integrating alongside existing shadcn components; inspect Tailwind v4 token mappings and portal focus behavior.
**Primary sources:** [Source 1](https://coss.com/ui) · [Source 2](https://github.com/cosscom/ui)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component, block, component-family, visual-component; forms: base-ui-particles, coordinated-controls, product-blocks.

### Cult UI (`cult-ui`)

Design-engineer React, Tailwind CSS and Motion blocks, expandable surfaces and interactive cards.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Interactive docs, source code, shadcn-compatible installs and public GitHub repository.
**Adoption judgment:** Verify free vs separately distributed items, check Motion/Tailwind dependencies and inspect keyboard focus and touch parity on hover-driven effects.
**Primary sources:** [Source 1](https://github.com/nolly-studio/cult-ui)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: visual-component, block, effect; forms: tactile-cards, expandable-blocks, motion-compositions.

### Design Spells (`design-spells`)

Curated archive of micro-interactions, subtle state transitions and memorable UI craft details.

**Find by:** design-reference, motion. **Form:** reference. **Stack scope:** reference.
**Access:** Public video/clip gallery organized by product and interaction detail.
**Adoption judgment:** Study trigger timing, feedback clarity and restraint so micro-interactions reinforce task comprehension rather than distracting from core workflows.
**Primary sources:** [Source 1](https://www.designspells.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: effect, interaction-mechanism, component; forms: micro-interaction-clips, state-transition-craft-details.

### Embla Carousel (`embla`)

Controlled carousel movement, dragging and slide relationships.

**Find by:** motion, controls. **Form:** package, engine. **Stack scope:** javascript, multi-framework.
**Access:** Examples, parameter guides and framework packages.
**Adoption judgment:** Use a carousel when it serves the content; check focus, touch, autoplay and reduced motion.
**Primary sources:** [Source 1](https://www.embla-carousel.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: interaction-mechanism, effect; forms: physics-carousel-track, drag-slide-motion.

### fffuel (`fffuel`)

Curated suite of SVG noise/grain, mesh gradient, organic shape and geometric pattern generators.

**Find by:** imagery, visual-effects, foundations. **Form:** generator, asset. **Stack scope:** framework-neutral, html-css.
**Access:** Browser-based parametric SVG/CSS generators with direct SVG and code copy.
**Adoption judgment:** Optimize exported SVG markup, keep texture opacity subtle enough to preserve text legibility and check filter performance (such as feTurbulence) on mobile GPUs.
**Primary sources:** [Source 1](https://www.fffuel.co/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, implementation-route; potential scope: imagery, effect; forms: svg-grain-textures, mesh-gradients, geometric-patterns.

### Finesse UI (`finesse`)

Figma component, variant and page-composition reference.

**Find by:** design-reference, layout, foundations. **Form:** design-file, reference. **Stack scope:** design-tool.
**Access:** Design-kit catalog and Figma entry.
**Adoption judgment:** Treat it as a design file; verify purchase/access and any implementation or asset rights.
**Primary sources:** [Source 1](https://finesseui.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: design-reference; potential scope: page, component-family; forms: design-file-not-runtime-implementation.
Finesse UI at finesseui.com is a design-kit entry, not mouse-lin/finesse-skill. The latter is a separately attributed method source, not an adopted UI component.

### Floating UI (`floating-ui`)

Floating-element alignment, collision and available-space handling.

**Find by:** controls. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** Live examples, positioning APIs and packages.
**Adoption judgment:** Assign positioning and complete control semantics separately; check scroll containers and layer ownership.
**Primary sources:** [Source 1](https://floating-ui.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: interaction-mechanism; forms: floating-positioning-and-collision-engine.

### Fonts In Use (`fonts-in-use`)

Searchable archive of real-world typographic art direction, editorial layouts and typeface pairings.

**Find by:** design-reference, typography. **Form:** reference. **Stack scope:** reference.
**Access:** Public archive searchable by typeface, industry, format and topic.
**Adoption judgment:** Use as typographic art-direction and pairing evidence; confirm licensing and web-rendering behavior of any identified commercial typeface or select an appropriately licensed substitute.
**Primary sources:** [Source 1](https://fontsinuse.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: typography, page; forms: real-world-type-specimens, typographic-pairings.

### Fontshare (`fontshare`)

Free curated editorial, display and neo-grotesque font service by Indian Type Foundry (e.g. Satoshi, Clash Display, Switzer, Cabinet Grotesk, Boska).

**Find by:** typography, foundations. **Form:** font, reference. **Stack scope:** framework-neutral.
**Access:** Type specimen catalog, variable font downloads, CSS delivery and pairing previews.
**Adoption judgment:** Verify individual typeface license terms (ITF Free Font License vs commercial variants), inspect script/diacritic coverage and pair with local CJK fallback fonts where multilingual text is required.
**Primary sources:** [Source 1](https://www.fontshare.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, discovery-and-reference; potential scope: typography; forms: editorial-display-typefaces, neo-grotesque-families, variable-fonts.

### Fontsource (`fontsource`)

Self-hosted font families, weights, subsets and variable fonts.

**Find by:** typography. **Form:** font, package. **Stack scope:** framework-neutral.
**Access:** Font catalog, llms index/full docs, page Markdown and font API docs.
**Adoption judgment:** AI docs cover usage and exclude generated font catalog pages. Inspect actual family/glyph coverage and individual font terms separately.
**Primary sources:** [Source 1](https://fontsource.org/docs/getting-started/introduction) · [Source 2](https://fontsource.org/docs/getting-started/ai-and-llms)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: implementation-route, visual-implementation; potential scope: typography; forms: self-hosted-fonts, variable-typefaces.

### Fumadocs (`fumadocs`)

High-craft documentation and editorial shell framework for React and Next.js with search, TOC and MDX components.

**Find by:** layout, typography, complex-information. **Form:** package, system, blocks. **Stack scope:** react.
**Access:** Documentation, starter templates, packages and open-source GitHub repository.
**Adoption judgment:** Confirm framework router compatibility (Next.js App Router, React Router, TanStack Start), customize typography and surface tokens so the docs shell fits the host product identity.
**Primary sources:** [Source 1](https://www.fumadocs.dev/) · [Source 2](https://github.com/fuma-nama/fumadocs)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: page, block, component-family, typography; forms: editorial-documentation-shell, sidebar-toc-search-system.

### Godly (`godly`)

High-craft web design gallery indexed by both complete websites and section-level UI compositions.

**Find by:** design-reference, layout, visual-effects. **Form:** reference. **Stack scope:** reference.
**Access:** Public website and section galleries with video/motion previews and live site links.
**Adoption judgment:** Use the sections index to compare hero, bento, pricing and footer composition craft directly; check live sites for motion cost, foreground contrast and real content density.
**Primary sources:** [Source 1](https://godly.design/websites/) · [Source 2](https://godly.design/sections/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: page, block, effect; forms: high-craft-websites, section-level-ui-compositions.

### GSAP (`gsap`)

Timelines, scroll, text and coordinated multi-element motion.

**Find by:** motion, typography. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** llms index, core/plugin APIs and examples.
**Adoption judgment:** Check scope, teardown, reduced motion, repeated interaction and applicable license.
**Primary sources:** [Source 1](https://gsap.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: implementation-route; potential scope: effect, timeline; forms: sequencing-engine.

### Iconify (`iconify`)

Search and distribute icons across multiple collections.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral.
**Access:** Collection directory, APIs, components and offline icon data.
**Adoption judgment:** Check each collection license and visual fit; choose online retrieval or local bundling deliberately.
**Primary sources:** [Source 1](https://iconify.design/docs/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: discovery-and-reference, implementation-route; potential scope: icons; forms: multi-collection-icon-directory, svg-delivery.

### Inspira UI (`inspira`)

Copyable Vue/Nuxt backgrounds, text, interaction and display components.

**Find by:** visual-effects, motion, layout. **Form:** source, visual-component. **Stack scope:** vue.
**Access:** Category documentation, demos/source and installation guide.
**Adoption judgment:** Match Vue, Tailwind and motion-library versions with the selected component documentation.
**Primary sources:** [Source 1](https://docs.inspira-ui.com/docs/en) · [Source 2](https://docs.inspira-ui.com/docs/en/getting-started/installation)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, cards, visual-interaction. **Profile sources:** [Source 1](https://inspira-ui.com/docs) · [Source 2](https://inspira-ui.com/docs/getting-started/installation)

### Kokonut UI (`kokonut-ui`)

Tailwind CSS and Motion interactive cards, tactile controls and expressive UI blocks.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Component catalog, live previews, copyable source, registry install and public GitHub repository.
**Adoption judgment:** Inspect settled-card text crispness and flatten resting 3D transforms (translateZ/perspective/will-change) if subpixel blur appears; check Motion bundle footprint, reduced-motion handling and mobile viewport height.
**Primary sources:** [Source 1](https://kokonutui.com/) · [Source 2](https://github.com/kokonut-labs/kokonutui)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: visual-component, block, effect; forms: interactive-cards, motion-blocks, tactile-controls.

### Lenis (`lenis`)

Smooth scroll interpolation engine by Darkroom Engineering for editorial and choreographed scroll experiences.

**Find by:** motion, layout. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** Documentation, framework wrappers, demos and open-source GitHub repository.
**Adoption judgment:** Verify native keyboard scrolling, trackpad/wheel latency, hash anchor jumps, nested scroll containers, browser scroll restoration and prefers-reduced-motion bypass before enabling globally.
**Primary sources:** [Source 1](https://lenis.dev/) · [Source 2](https://github.com/darkroomengineering/lenis)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: implementation-route; potential scope: interaction-mechanism, effect; forms: smooth-scroll-interpolation.

### LottieFiles (`lottiefiles`)

Graphic animation, loaders and feedback assets.

**Find by:** motion, imagery. **Form:** asset, engine. **Stack scope:** multi-runtime.
**Access:** Asset catalog, developer docs and framework/player integrations.
**Adoption judgment:** Check asset and player licenses separately; assess payload, renderer support and communicative value.
**Primary sources:** [Source 1](https://lottiefiles.com/developers)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: discovery-and-reference, implementation-route; potential scope: effect, imagery; forms: authored-vector-animation, loaders, feedback-graphics.

### Lucide (`lucide`)

Consistent line icons with framework-specific delivery options.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral.
**Access:** Icon catalog, framework guides, SVG and packages.
**Adoption judgment:** Match weight, size and accessible naming; retain an adequate interaction target around a small icon.
**Primary sources:** [Source 1](https://lucide.dev/guide/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: icons; forms: line-icon-family, svg-symbols.

### lucide-animated (`lucide-animated`)

Smoothly animated Lucide SVG icons powered by Motion for tactile micro-interaction feedback.

**Find by:** icons, motion. **Form:** source, asset, visual-component. **Stack scope:** react.
**Access:** Interactive icon preview gallery, copyable source, registry install and GitHub repository.
**Adoption judgment:** Reserve animated icons for purposeful state or hover confirmation rather than perpetual motion; verify reduced-motion fallback and align stroke weight with static Lucide icons in the same toolbar.
**Primary sources:** [Source 1](https://lucide-animated.com/) · [Source 2](https://github.com/pqoqubbw/icons)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: icons, visual-component, effect; forms: motion-animated-svg-icons, hover-and-state-icon-feedback.

### Magic UI (`magic-ui`)

Expressive effects, text, backgrounds and display blocks.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Component docs, Copy Page and documented MCP entry.
**Adoption judgment:** Identify the particular free component or separately sold template; review behavior and effect intensity in the complete page.
**Primary sources:** [Source 1](https://magicui.design/docs/mcp)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: visual-implementation; potential scope: visual-component, block; forms: border-light, text-motion, background, display-composition. **Profile sources:** [Source 1](https://magicui.design/docs/components/shine-border)

### Mantine (`mantine`)

Comprehensive React component library paired with prebuilt responsive UI blocks (ui.mantine.dev).

**Find by:** controls, layout, complex-information, foundations. **Form:** package, system, blocks. **Stack scope:** react.
**Access:** Component API docs, Mantine UI block gallery and package installation.
**Adoption judgment:** Match Mantine PostCSS/CSS-layer order with any coexisting utility CSS to avoid cascade collisions; customize theme radii, font family and surface tokens so products avoid stock appearance.
**Primary sources:** [Source 1](https://mantine.dev/) · [Source 2](https://ui.mantine.dev/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component-family, block, tokens; forms: coordinated-react-system, prebuilt-responsive-blocks.

### Mobbin (`mobbin`)

Product-screen and user-flow observation.

**Find by:** design-reference, layout. **Form:** reference. **Stack scope:** reference.
**Access:** Screen/flow search, visible previews and product records.
**Adoption judgment:** Use task and state relationships as reference; content access and permission to reuse product assets are separate.
**Primary sources:** [Source 1](https://mobbin.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: page, block; forms: shipped-product-screens, multi-step-user-flows.

### Motion (`motion`)

Transitions, gestures, layout changes and motion control.

**Find by:** motion. **Form:** package, engine. **Stack scope:** react, vue, javascript.
**Access:** Framework-specific docs/examples and separately authorized AI tooling.
**Adoption judgment:** Select APIs by interaction purpose and runtime; distinguish base capabilities from tools requiring additional access.
**Primary sources:** [Source 1](https://motion.dev/docs) · [Source 2](https://motion.dev/docs/ai-kit)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: implementation-route; potential scope: effect, interaction-mechanism; forms: animation-and-input-engine. **Profile sources:** [Source 1](https://motion.dev/docs/react-drag)

### Motion Primitives (`motion-primitives`)

Open-source React, Motion and Tailwind CSS motion primitives for text transitions, surfaces and micro-interactions.

**Find by:** motion, visual-effects, typography. **Form:** source, visual-component. **Stack scope:** react.
**Access:** Component demos, copyable source, CLI registry entries and MIT-licensed GitHub repository.
**Adoption judgment:** Match Motion library major version, verify prefers-reduced-motion behavior and test text-split/layout animations with real multiline and localized copy.
**Primary sources:** [Source 1](https://github.com/ibelick/motion-primitives)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, implementation-route; potential scope: visual-component, effect, interaction-mechanism; forms: text-motion, border-effects, spring-micro-interactions.

### MUI (`mui`)

Product components, themes and complex-interface foundations.

**Find by:** controls, layout, complex-information. **Form:** package, system. **Stack scope:** react.
**Access:** Component APIs/demos, AI documentation and MCP guide.
**Adoption judgment:** Check the specific package/version and any commercial extension terms.
**Primary sources:** [Source 1](https://mui.com/material-ui/getting-started/mcp/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component-family, tokens; forms: material-system, dense-controls, data-views.

### NumberFlow (`number-flow`)

Smoothly animated numeric, currency and percentage transitions with tabular digit choreography.

**Find by:** motion, typography. **Form:** package, visual-component. **Stack scope:** react, vue, svelte, javascript, multi-framework.
**Access:** Framework packages (React, Vue, Svelte, vanilla), interactive demos and GitHub repository.
**Adoption judgment:** Pair with tabular-nums font features and locale-aware Intl formatting; verify prefers-reduced-motion behavior and accessible live numeric announcements without announcement spam.
**Primary sources:** [Source 1](https://number-flow.barvian.me) · [Source 2](https://github.com/barvian/number-flow)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, implementation-route; potential scope: visual-component, effect, typography; forms: rolling-numeric-transitions, tabular-kpi-motion.

### Nuxt UI (`nuxt-ui`)

Product controls, themes, forms and layouts for Nuxt/Vue.

**Find by:** controls, layout, foundations. **Form:** package, system. **Stack scope:** vue.
**Access:** llms index, per-page Markdown, examples and MCP/Skill documentation links.
**Adoption judgment:** Match the installed version and theme mechanism; documented tools become usable through actual host connections.
**Primary sources:** [Source 1](https://ui.nuxt.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component-family, block, tokens; forms: coordinated-controls, themed-system, product-layouts.

### Observable Plot (`observable-plot`)

Publication-grade grammar-of-graphics library for concise, faceted statistical SVG data visualizations.

**Find by:** complex-information, imagery. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** Official documentation, gallery examples, package install and GitHub repository.
**Adoption judgment:** Wrap SVG output with explicit responsive container sizing, project typography tokens and accessible titles/descriptions or tabular fallbacks for screen readers.
**Primary sources:** [Source 1](https://observablehq.github.io/plot/) · [Source 2](https://github.com/observablehq/plot)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, implementation-route; potential scope: visual-component, imagery; forms: editorial-svg-charts, faceted-statistical-graphics.

### Open Props (`open-props`)

Reusable CSS sizes, spacing, colors, shadows and easing.

**Find by:** foundations, motion. **Form:** tokens. **Stack scope:** framework-neutral.
**Access:** Token directory, source and import guidance.
**Adoption judgment:** Map selected values into project semantic roles and one coherent set of scales.
**Primary sources:** [Source 1](https://open-props.style/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: tokens; forms: css-custom-properties, spacing-color-easing-scales.

### Paper Shaders (`paper-shaders`)

Parameterized textures, light, metal and dot-grid surfaces.

**Find by:** visual-effects. **Form:** package, demo. **Stack scope:** react.
**Access:** Live parameters and usage examples; the snapshot inspected React examples.
**Adoption judgment:** Review GPU cost, static equivalents, background pause and foreground contrast. Confirm the particular package and runtime.
**Primary sources:** [Source 1](https://shaders.paper.design/dot-grid) · [Source 2](https://shaders.paper.design/liquid-metal)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: effect, visual-component; forms: shader-surface, procedural-texture, background.

### Penpot (`penpot`)

Editable design structures, assets and token-to-code mapping.

**Find by:** design-reference, foundations, layout. **Form:** design-file, tool. **Stack scope:** design-tool.
**Access:** Design files, token export, official MCP and API.
**Adoption judgment:** Confirm the active document, read/write scope, permissions and host connection before operating on real files.
**Primary sources:** [Source 1](https://help.penpot.app/mcp/) · [Source 2](https://help.penpot.app/user-guide/design-systems/design-tokens/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, implementation-route; potential scope: page, tokens, component-family; forms: editable-design-files, design-tokens-mapping.

### Phosphor Icons (`phosphor-icons`)

Flexible icon family with six coordinated weights (thin, light, regular, bold, fill, duotone) across web frameworks.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral, multi-framework.
**Access:** Interactive icon picker, framework packages, raw SVG and open-source GitHub repository.
**Adoption judgment:** Commit to a deliberate weight mapping (for example regular for default actions and fill/duotone for active states) rather than mixing unrelated icon families; preserve accessible names and hit targets.
**Primary sources:** [Source 1](https://phosphoricons.com/) · [Source 2](https://github.com/phosphor-icons/homepage)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: icons; forms: six-weight-icon-family, duotone-and-fill-icons.

### Poly Haven (`poly-haven`)

CC0 library of HDRI environment maps, PBR material textures and 3D models.

**Find by:** imagery, visual-effects. **Form:** asset. **Stack scope:** framework-neutral, design-tool.
**Access:** Public asset library with resolution/format downloads and documented CC0 asset license.
**Adoption judgment:** Downloadable HDRIs, textures and 3D models are published under CC0, whereas Poly Haven site logos, branding and example renders remain separate from the CC0 asset license; downsample textures to fit web delivery budgets.
**Primary sources:** [Source 1](https://polyhaven.com/license)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: imagery, scene; forms: cc0-hdri-lighting, pbr-material-textures, 3d-models.

### prompt-kit (`prompt-kit`)

Core UI building blocks for AI chat composers, message streams and prompt workflows on shadcn/ui.

**Find by:** controls, layout, complex-information. **Form:** source, blocks, registry. **Stack scope:** react.
**Access:** Component documentation, demos, shadcn registry install and GitHub repository.
**Adoption judgment:** Test multiline composer growth, scroll-to-bottom anchoring during streaming, mobile keyboard viewport height and real backend error/cancel states.
**Primary sources:** [Source 1](https://github.com/ibelick/prompt-kit)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: block, component; forms: ai-prompt-composers, chat-message-blocks, streaming-response-ui.

### Radix Colors (`radix-colors`)

Color scales for surfaces, boundaries, emphasis and text across themes.

**Find by:** foundations. **Form:** tokens, package. **Stack scope:** framework-neutral.
**Access:** Color/use guidance and source/package access.
**Adoption judgment:** Map colors to actual roles and verify contrast in real combinations.
**Primary sources:** [Source 1](https://www.radix-ui.com/colors)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: tokens; forms: perceptual-color-scales, light-dark-surface-ramps.

### Radix Primitives (`radix-primitives`)

Composable menus, dialogs, selection and focus behavior.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** react.
**Access:** Categorized APIs, examples and interaction/accessibility documentation.
**Adoption judgment:** Preserve semantic/state contracts and map styling into project tokens; confirm package names for the selected version.
**Primary sources:** [Source 1](https://www.radix-ui.com/primitives/docs/overview/introduction)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.

### React Aria (`react-aria`)

Input, collection, form and internationalized interaction capabilities.

**Find by:** controls, complex-information. **Form:** package, primitive. **Stack scope:** react.
**Access:** Component APIs, examples and styling guides.
**Adoption judgment:** Evaluate primitive behavior and the complete page separately; use the correct package and state model.
**Primary sources:** [Source 1](https://react-aria.adobe.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.

### React Bits (`react-bits`)

Animated backgrounds, text, interactions and expressive display components.

**Find by:** visual-effects, motion, typography. **Form:** source, demo, visual-component. **Stack scope:** react.
**Access:** Index, category demos, source variants and documented component installation.
**Adoption judgment:** Select exact JS/TS and CSS/Tailwind variants; inspect the actual animation/rendering dependencies and preserve demonstration parameters.
**Primary sources:** [Source 1](https://reactbits.dev/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, card-material, pointer-response. **Profile sources:** [Source 1](https://reactbits.dev/) · [Source 2](https://reactbits.dev/components/spotlight-card)

### React Three Fiber & Drei (`react-three-fiber`)

Declarative React renderer for Three.js paired with Drei helpers for lighting, cameras, shaders and spatial controls.

**Find by:** visual-effects, imagery, motion. **Form:** package, engine. **Stack scope:** react.
**Access:** Documentation sites, packages and public Pmndrs GitHub repositories.
**Adoption judgment:** Match React and Three.js major versions, budget GPU/battery load with on-demand frameloop or static poster fallbacks and verify reduced-motion and WebGL-unavailable degradation.
**Primary sources:** [Source 1](https://r3f.docs.pmnd.rs/) · [Source 2](https://drei.docs.pmnd.rs/) · [Source 3](https://github.com/pmndrs/react-three-fiber) · [Source 4](https://github.com/pmndrs/drei)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: implementation-route; potential scope: scene, effect; forms: declarative-webgl-scenes, 3d-lighting-and-materials.

### Recharts (`recharts`)

Composable React SVG charting library for line, bar, area, radar and scatter visualizations.

**Find by:** complex-information, imagery. **Form:** package, engine. **Stack scope:** react.
**Access:** API docs, live chart examples and package installation.
**Adoption judgment:** Verify responsive container sizing on initial mount/SSR, customize axis typography and tooltip surfaces to project tokens and check high-series-count SVG performance.
**Primary sources:** [Source 1](https://recharts.github.io/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: visual-component, imagery; forms: composable-svg-charts, responsive-data-series.

### Refero (`refero`)

Real shipped web product UI screens and multi-step user-flow reference archive.

**Find by:** design-reference, layout. **Form:** reference. **Stack scope:** reference.
**Access:** Searchable screen/flow gallery filtered by UI pattern, product type and page role.
**Adoption judgment:** Use to study real product conventions, navigation hierarchy and state transitions; screenshots are design-reference evidence, not permission to copy proprietary branding or rebuild without mature implementation sources.
**Primary sources:** [Source 1](https://refero.design/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: page, block; forms: shipped-web-product-screens, multi-screen-user-flows.

### Reka UI (`reka`)

Vue menus, overlays, inputs and focus behavior.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** vue.
**Access:** Component APIs, examples and Markdown documentation entry.
**Adoption judgment:** Compose stable interaction with tailored appearance; confirm controlled state and event wiring.
**Primary sources:** [Source 1](https://reka-ui.com/docs/overview/introduction)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.

### Rive (`rive`)

Designer-authored state-driven graphics and interactive animation.

**Find by:** motion, imagery. **Form:** asset, engine. **Stack scope:** multi-runtime.
**Access:** Runtime documentation, platform capability guides and animation files.
**Adoption judgment:** Check authoring access, asset rights and selected runtime capability/version separately.
**Primary sources:** [Source 1](https://rive.app/docs/runtimes/getting-started)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: implementation-route, visual-implementation; potential scope: effect, interaction-mechanism, scene; forms: state-machine-animation, interactive-vector.

### shadcn-svelte (`shadcn-svelte`)

Editable Svelte and Bits UI component registry, accessible controls and product blocks.

**Find by:** controls, layout. **Form:** source, blocks, registry. **Stack scope:** svelte.
**Access:** Component documentation, CLI registry install and public GitHub repository.
**Adoption judgment:** Confirm Svelte 5 / Bits UI version compatibility and Tailwind token configuration before installing; copied components carry local maintenance ownership.
**Primary sources:** [Source 1](https://github.com/huntabyte/shadcn-svelte)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component, block; forms: coordinated-controls, svelte-product-blocks.

### shadcn-vue (`shadcn-vue`)

Editable Vue product components and blocks.

**Find by:** controls, layout. **Form:** source, blocks, registry. **Stack scope:** vue.
**Access:** Component documentation, registry/CLI and MCP guide.
**Adoption judgment:** Select the Vue source, CLI and dependencies explicitly; distribution schema and framework compatibility are separate facts.
**Primary sources:** [Source 1](https://www.shadcn-vue.com/docs/mcp)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation, visual-implementation; potential scope: component, block; forms: coordinated-controls, product-blocks.

### shadcn/ui (`shadcn`)

Product components and blocks delivered as editable source.

**Find by:** controls, layout. **Form:** source, blocks, registry. **Stack scope:** react.
**Access:** llms index, demos/APIs, registry, CLI inspection/preview and MCP docs.
**Adoption judgment:** Inspect files, dependencies and global CSS changes before installation; copied source has local maintenance ownership.
**Primary sources:** [Source 1](https://ui.shadcn.com/llms.txt) · [Source 2](https://ui.shadcn.com/docs/cli) · [Source 3](https://ui.shadcn.com/docs/registry/registry-item-json)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: functional-foundation, visual-implementation; potential scope: component, block; forms: coordinated-controls, product-blocks.

### SiteInspire (`siteinspire`)

Curated directory of interactive, editorial and minimalist web design with faceted style and subject filters.

**Find by:** design-reference, layout. **Form:** reference. **Stack scope:** reference.
**Access:** Public faceted website gallery linking directly to live sites.
**Adoption judgment:** Use to benchmark grid restraint, whitespace proportion and editorial pacing across industries; inspect live sites across desktop and mobile viewports rather than judging thumbnails alone.
**Primary sources:** [Source 1](https://www.siteinspire.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: page, block; forms: editorial-and-minimalist-websites, grid-and-pacing-references.

### SmoothUI (`smoothui`)

Animated React and Tailwind CSS micro-interaction components and spring-driven UI controls.

**Find by:** motion, controls, visual-effects. **Form:** source, visual-component. **Stack scope:** react.
**Access:** Interactive component catalog, live demos and copyable source snippets.
**Adoption judgment:** Inspect spring stiffness, focus-visible rings, keyboard operation and mobile touch targets when adapting showcase micro-interactions into production controls.
**Primary sources:** [Source 1](https://smoothui.dev/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: visual-component, component, effect; forms: micro-interactions, animated-controls, spring-transitions.

### Sonner (`sonner`)

Opinionated stacked toast notification component with swipe-to-dismiss and promise states.

**Find by:** controls, motion. **Form:** package, visual-component. **Stack scope:** react.
**Access:** Package installation, API documentation and open-source GitHub repository.
**Adoption judgment:** Coordinate toast styling with project surface tokens, configure accessible live-region politeness and verify z-index layering above dialogs and drawers.
**Primary sources:** [Source 1](https://github.com/emilkowalski/sonner)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: visual-component, component, interaction-mechanism; forms: stacked-toast-notifications, gesture-dismiss-feedback.

### Spline (`spline`)

Interactive 3D scene authoring tool supporting static image, video and WebGL runtime exports.

**Find by:** visual-effects, imagery, motion. **Form:** tool, asset, engine. **Stack scope:** multi-runtime, design-tool.
**Access:** Design tool, export FAQ/docs and framework runtime embeds.
**Adoption judgment:** Choose static render, pre-rendered video or live WebGL export by actual interaction need and payload budget; verify account export rights, watermark terms and fallback states.
**Primary sources:** [Source 1](https://spline.design/) · [Source 2](https://docs.spline.design/basics/faq)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, visual-implementation, implementation-route; potential scope: scene, imagery, effect; forms: authored-3d-scenes, static-video-or-webgl-exports.

### Tabler Icons (`tabler-icons`)

Extensive MIT-licensed library of 6,500+ SVG icons with customizable stroke width across React, Vue, Svelte, Solid and HTML.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral, multi-framework.
**Access:** Icon browser, framework packages, raw SVG downloads and GitHub repository.
**Adoption judgment:** Standardize stroke-width across sizes so small 16px icons stay crisp without clogging; import individual tree-shaken icons rather than bundling the full sprite.
**Primary sources:** [Source 1](https://tabler.io/icons) · [Source 2](https://github.com/tabler/tabler-icons)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: icons; forms: customizable-stroke-svg-icons, filled-and-outline-glyphs.

### Tailark (`tailark`)

Marketing and landing-page sections built on shadcn/ui and Tailwind CSS.

**Find by:** layout. **Form:** source, blocks, registry. **Stack scope:** react.
**Access:** Section gallery, responsive previews, registry install and public GitHub blocks repository.
**Adoption judgment:** De-template showcase placeholder copy and generic palettes; harmonize section typography, spacing cadence and semantic color tokens with the product identity.
**Primary sources:** [Source 1](https://tailark.com/) · [Source 2](https://github.com/tailark/blocks)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: block, page; forms: marketing-sections, hero-compositions, pricing-and-feature-grids.

### TanStack Table (`tanstack-table`)

Headless sorting, filtering, columns and table state.

**Find by:** complex-information. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** Framework-adapter docs, APIs and examples.
**Adoption judgment:** Choose behavior and appearance separately; test actual data scale, keyboard behavior and server-query boundaries.
**Primary sources:** [Source 1](https://tanstack.com/table/latest)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation; potential scope: interaction-mechanism; forms: headless-table-state-visual-treatment-selected-separately.

### The Component Gallery (`component-gallery`)

Cross-design-system component taxonomy and live directory of public design systems.

**Find by:** design-reference, controls, foundations. **Form:** reference. **Stack scope:** reference.
**Access:** Public component-by-component comparison pages and live design-system index.
**Adoption judgment:** Use to compare naming conventions, anatomy, accessibility states and variant coverage across mature public design systems before finalizing component contracts.
**Primary sources:** [Source 1](https://component.gallery/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: component-family, component, tokens; forms: cross-system-component-taxonomy, live-design-system-directory.

### Tiptap (`tiptap`)

Extensible rich-text and structured editing.

**Find by:** complex-information. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** APIs, extension directory, framework guides and examples.
**Adoption judgment:** Check editor state, content format, persistence and extension rights against the real scope.
**Primary sources:** [Source 1](https://tiptap.dev/docs/editor/getting-started/overview)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: component, interaction-mechanism; forms: headless-rich-text-editor-visual-chrome-selected-separately.

### tldraw (`tldraw`)

Infinite whiteboard and spatial canvas SDK with vector drawing, multiplayer primitives and custom shapes.

**Find by:** complex-information, layout, imagery. **Form:** package, engine. **Stack scope:** react.
**Access:** SDK documentation, interactive examples, packages and public GitHub repository.
**Adoption judgment:** Verify the tldraw commercial/source-available license and watermark or production license requirements explicitly before adopting; inspect bundle weight and keyboard/touch canvas ergonomics.
**Primary sources:** [Source 1](https://tldraw.dev/) · [Source 2](https://github.com/tldraw/tldraw)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation, implementation-route; potential scope: page, scene, interaction-mechanism; forms: infinite-spatial-whiteboard, vector-drawing-canvas.

### Tremor (`tremor`)

Dashboard blocks, KPI cards and chart components built with Tailwind CSS and Radix Primitives.

**Find by:** complex-information, layout, controls. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Copyable component source, dashboard blocks, documentation and GitHub repository.
**Adoption judgment:** Check free components vs separately licensed blocks, align chart palettes with project semantic tokens and verify numeric alignment and dense-data readability on narrow viewports.
**Primary sources:** [Source 1](https://tremor.so/) · [Source 2](https://github.com/tremorlabs/tremor)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: block, visual-component, component-family; forms: kpi-cards, analytics-dashboard-blocks, data-charts.

### tweakcn (`tweakcn`)

OKLCH theme presets and interactive semantic token editor for shadcn/ui and Tailwind CSS v4.

**Find by:** foundations. **Form:** tokens, generator, reference. **Stack scope:** react, framework-neutral.
**Access:** Live theme previewer, CSS custom property export, presets and open-source GitHub repository.
**Adoption judgment:** Verify WCAG contrast ratios across light and dark semantic pairs under real text sizes, and map exported variables into one canonical project token plane.
**Primary sources:** [Source 1](https://tweakcn.com/) · [Source 2](https://github.com/jnsahaj/tweakcn)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, discovery-and-reference; potential scope: tokens; forms: oklch-color-themes, semantic-token-presets, surface-elevation-ramps.

### Typewolf (`typewolf`)

Curated archive of real-world web typography pairings, live site specimens and font-stack notes.

**Find by:** design-reference, typography. **Form:** reference. **Stack scope:** reference.
**Access:** Public site-of-the-day archive, typeface pages and pairing guides.
**Adoption judgment:** Inspect the live specimen sites to evaluate actual rendering scale, line-height and measure; verify webfont licensing before adopting any commercial display or text family.
**Primary sources:** [Source 1](https://www.typewolf.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, discovery-and-reference; potential scope: typography, page; forms: curated-web-font-pairings, live-site-type-specimens.

### Uiverse (`uiverse`)

Community examples for buttons, loaders, forms and cards.

**Find by:** controls, visual-effects. **Form:** source, reference. **Stack scope:** html-css, react.
**Access:** Category search, live preview and item code.
**Adoption judgment:** Assess each author/item for semantics, license and maintainability; gallery membership identifies a lead.
**Primary sources:** [Source 1](https://uiverse.io/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: discovery-and-reference, visual-implementation; potential scope: component, visual-component, effect; forms: community-controls, loaders, cards, css-effects.

### unDraw (`undraw`)

Subject illustrations with adjustable accent color.

**Find by:** imagery. **Form:** asset. **Stack scope:** framework-neutral.
**Access:** Browse/search, color preview and download.
**Adoption judgment:** Check original asset terms for the actual product use and any redistribution/platform integration.
**Primary sources:** [Source 1](https://undraw.co/) · [Source 2](https://undraw.co/license)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation; potential scope: imagery; forms: recolorable-flat-svg-illustrations.

### Unicorn Studio (`unicorn-studio`)

Interactive WebGL shader scene authoring and embeddable visual backgrounds.

**Find by:** visual-effects, motion, imagery. **Form:** tool, asset, demo. **Stack scope:** javascript, framework-neutral.
**Access:** Web authoring tool, hosted/exported WebGL runtime embeds and interactive showcase demos.
**Adoption judgment:** Check account/export license terms, pause offscreen rendering, supply a static poster/fallback for WebGL-restricted or reduced-motion devices and verify foreground text contrast.
**Primary sources:** [Source 1](https://www.unicorn.studio/)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, implementation-route; potential scope: scene, effect, imagery; forms: interactive-webgl-backgrounds, layered-shader-scenes.

### Unsplash (`unsplash`)

Editorial photography library for art-directed imagery, backgrounds and product storytelling.

**Find by:** imagery. **Form:** asset. **Stack scope:** framework-neutral.
**Access:** Searchable photography catalog, API guidelines and public license page.
**Adoption judgment:** Verify the exact item tier (free vs Unsplash+) and any model, property or trademark permissions required by the product context; avoid uncached hotlinking and inspect real aspect-ratio crops.
**Primary sources:** [Source 1](https://unsplash.com/license)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: visual-implementation, discovery-and-reference; potential scope: imagery; forms: editorial-photography, subject-imagery.

### Utopia (`utopia`)

Fluid type, space and grid tools.

**Find by:** foundations, typography, layout. **Form:** generator, reference. **Stack scope:** framework-neutral.
**Access:** Generators, method guidance and CSS output.
**Adoption judgment:** Calibrate generated bounds to real content and device conditions; parameters are design choices.
**Primary sources:** [Source 1](https://utopia.fyi/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: design-reference, implementation-route; potential scope: tokens, typography; forms: fluid-type-scales, fluid-space-and-grid.

### Vaul (`vaul`)

Touch-physics drawer and bottom-sheet primitive with snap points and background scaling.

**Find by:** controls, motion. **Form:** package, primitive. **Stack scope:** react.
**Access:** Package installation, usage examples and GitHub repository.
**Adoption judgment:** Check the upstream README maintenance status (the author has marked Vaul unmaintained and points to alternatives such as Base UI); verify explicit aria-modal, DialogTitle, focus return and mobile keyboard viewport behavior in the project.
**Primary sources:** [Source 1](https://github.com/emilkowalski/vaul)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: primitive, interaction-mechanism; forms: touch-physics-drawer, bottom-sheet-snap-points.

### Vue Bits (`vue-bits`)

Animated backgrounds, text, cards and visual interactions.

**Find by:** visual-effects, motion, layout. **Form:** source, demo, visual-component. **Stack scope:** vue.
**Access:** Category demos, configuration/source, Copy for AI, documented registry/MCP and a source-linked llms index.
**Adoption judgment:** The snapshot located llms.txt in official source; its direct fetch was unavailable. Check the exact MIT + Commons Clause terms and host tool availability for adoption.
**Primary sources:** [Source 1](https://vue-bits.dev/get-started/mcp) · [Source 2](https://vue-bits.dev/text-animations/fold-text) · [Source 3](https://github.com/DavidHDev/vue-bits/blob/3766ebeeed37ec35bce29f001b6d101c7b17da35/src/utils/aiExport.ts) · [Source 4](https://github.com/DavidHDev/vue-bits/blob/main/README.md)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-10-28): roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, cards, interaction. **Profile sources:** [Source 1](https://vue-bits.dev/)

### Web Awesome (`web-awesome`)

Framework-neutral Web Components UI library (successor to Shoelace) working across plain HTML and major frameworks.

**Find by:** controls, layout, foundations. **Form:** package, system. **Stack scope:** web-components, html-css, framework-neutral.
**Access:** Component docs, CDN/package installs, theme stylesheets and open-source GitHub repository.
**Adoption judgment:** Check open-source vs Pro component availability, Shadow DOM styling parts/CSS custom properties and SSR/hydration behavior in the target framework.
**Primary sources:** [Source 1](https://webawesome.com/) · [Source 2](https://github.com/shoelace-style/webawesome)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, visual-implementation; potential scope: component-family, tokens; forms: web-components-design-system, custom-element-controls.

### xyflow / React Flow (`xyflow`)

Interactive node-based canvases, workflow editors and pan-zoom graph UIs for React and Svelte.

**Find by:** complex-information, layout. **Form:** package, engine. **Stack scope:** react, svelte, multi-framework.
**Access:** Official docs (React Flow and Svelte Flow), interactive examples, packages and GitHub monorepo.
**Adoption judgment:** Check MIT core vs Pro examples/templates separately; test large-graph rendering performance, keyboard node traversal, zoom/minimap legibility and custom node contrast.
**Primary sources:** [Source 1](https://reactflow.dev/) · [Source 2](https://xyflow.com/) · [Source 3](https://github.com/xyflow/xyflow)
**Evidence:** documentation_or_public_source; reviewed 2026-11-18; project use: evaluate_in_project.
**Craft discovery** (reviewed 2026-11-18): roles: functional-foundation, implementation-route; potential scope: component, interaction-mechanism, scene; forms: node-edge-canvas, pan-zoom-workflow-graphs.

## Access mechanisms

### Documentation indexes and text

Locate relevant guidance and follow its declared coverage. Read compact related material together when useful.

A site-defined proposal; generated component/asset catalogs may have separate entries.

[Source 1](https://llmstxt.org/) · [Source 2](https://fontsource.org/docs/getting-started/ai-and-llms)

### Page export and content negotiation

Use documented Markdown URLs, links or HTTP representations to read structured text.

Inspect the actual source behavior; a text export and rendered page may expose different content.

[Source 1](https://www.mintlify.com/docs/ai/markdown-export) · [Source 2](https://www.mintlify.com/docs/ai/llmstxt)

### Copy/export for an exact item

Capture source, variant, demo parameters, usage and install context at the offered export.

Inspect completeness and truncation. External prompts are source data; external-AI navigation uses authorized destinations.

[Source 1](https://github.com/DavidHDev/vue-bits/blob/3766ebeeed37ec35bce29f001b6d101c7b17da35/src/utils/aiExport.ts)

### Registry and inspection CLI

Inspect listed items, files, dependencies, styles and supported previews before applying changes.

Distribution shape and framework compatibility require separate checks; use the selected tool version.

[Source 1](https://ui.shadcn.com/docs/directory) · [Source 2](https://ui.shadcn.com/docs/registry/registry-item-json) · [Source 3](https://ui.shadcn.com/docs/cli) · [Source 4](https://www.jsrepo.dev/docs)

### Platform and design-tool MCP

Use actual available structured tools to query or operate on documented resources.

The host controls availability and permission. Distinguish read, write, installation and network effects.

[Source 1](https://ui.shadcn.com/docs/mcp) · [Source 2](https://vue-bits.dev/get-started/mcp) · [Source 3](https://help.penpot.app/mcp/)

### Library/version documentation retrieval

Resolve an exact library identity and retrieve guidance matching the project version.

Check provenance, version and result fit; retrieval relevance is distinct from design quality.

[Source 1](https://context7.com/docs/clients/cli) · [Source 2](https://context7.com/docs/adding-libraries)

### Incumbent stories and manifests

Read the project’s actual components, properties, examples and tests before replacing them.

Check the current host/framework support of optional AI tooling; normal stories remain useful independently.

[Source 1](https://storybook.js.org/docs/ai/mcp/overview) · [Source 2](https://storybook.js.org/docs/ai/manifests)

## Maintenance

The structured catalog is the maintained source; this map is generated from it. Preserve source identity, actual evidence scope and original observation dates. Recheck relevant version, rights, interface and availability when adopting. The release-specific spot checks are recorded in the data without changing every entry’s historical review date.
