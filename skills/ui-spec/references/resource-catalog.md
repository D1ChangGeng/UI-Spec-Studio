# UI resource map

Find a useful starting point by need, then read the exact item and its current primary source.
Apply [the common sourcing method](component-sourcing.md) throughout selection and integration.

Research snapshot: **2026-10-24** · **37 resources** · **7 access mechanisms**.
Curated from the accepted 2026-10-24 documentation/public-source research. The selected entries require current item, demo and project verification.

## Use the map

Read the relevant section, use the [structured catalog](../assets/resource-catalog.json), or query the optional local helper:

```bash
python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
python <skill-dir>/scripts/find_resources.py --list-filters
```

Queries match all supplied terms; filters combine. Results are alphabetical discovery leads. A stack filter includes framework-neutral candidates; exact adapter compatibility is checked in primary documentation. A missing match invites wider research. The helper reads local data and performs no installation or network operation.

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

**Reuse Scope** and **Visual Completeness** are independent. The former locates useful responsibility; the latter requires observing the exact item. A broad primitive library does not settle visual craft, and a resolved small effect does not settle a complete page.

Search complete pages and functional blocks when composition is the need; search visual components and assets when their material or motion supplies the defining relationship. Functional foundations and lower-level engines can complement them. These are open routes, not a required search order.

```bash
python <skill-dir>/scripts/find_resources.py --form visual-component --stack vue --json
python <skill-dir>/scripts/find_resources.py --form blocks --stack react --json
python <skill-dir>/scripts/find_resources.py --id react-bits --json
```

The visual-component filter identifies documented delivery form, not inspected quality. Read the original demo, exact source/configuration and use-time terms; continue outside this catalog when worthwhile. The installed inspector does not score or approve any choice.

| Resource | Documented role | Potential reuse scope | Visual search forms |
|---|---|---|---|
| 21st.dev | discovery-and-reference | page, block, component | author-specific-compositions |
| Aceternity UI | visual-implementation | visual-component, block | spotlight, cards, scroll-effects, typography |
| Base UI | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| Finesse UI | design-reference | page, component-family | design-file-not-runtime-implementation |
| GSAP | implementation-route | effect, timeline | sequencing-engine |
| Inspira UI | visual-implementation | visual-component, effect | background, text-motion, cards, visual-interaction |
| Magic UI | visual-implementation | visual-component, block | border-light, text-motion, background, display-composition |
| Motion | implementation-route | effect, interaction-mechanism | animation-and-input-engine |
| Radix Primitives | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| React Aria | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| React Bits | visual-implementation | visual-component, effect | background, text-motion, card-material, pointer-response |
| Reka UI | functional-foundation | primitive, component-family | visual-treatment-to-be-selected-in-context |
| shadcn-vue | functional-foundation, visual-implementation | component, block | coordinated-controls, product-blocks |
| shadcn/ui | functional-foundation, visual-implementation | component, block | coordinated-controls, product-blocks |
| Vue Bits | visual-implementation | visual-component, effect | background, text-motion, cards, interaction |

Finesse UI (finesseui.com) is a design-kit entry. The separately studied mouse-lin/finesse-skill is a method source, not that kit or a bundled runtime implementation.

## Resource cards

### 21st.dev (`21st`)

Community component, block, theme and template discovery.

**Find by:** layout, visual-effects. **Form:** source, blocks, reference. **Stack scope:** react.
**Access:** Search/catalog, previews and item-specific installation or prompt export.
**Adoption judgment:** Resolve original author/source, access terms and source completeness before adoption.
**Primary sources:** [Source 1](https://21st.dev/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: discovery-and-reference; potential scope: page, block, component; forms: author-specific-compositions.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://21st.dev/)

### Aceternity UI (`aceternity`)

Backgrounds, cards, scroll effects, text and showcase compositions.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Visual catalog, demos, usage code and component docs.
**Adoption judgment:** Review exact source, rights, dependencies and touch behavior; adapt strong effects to the accepted visual direction.
**Primary sources:** [Source 1](https://ui.aceternity.com/components)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: visual-implementation; potential scope: visual-component, block; forms: spotlight, cards, scroll-effects, typography.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://ui.aceternity.com/components/spotlight-new) · [Source 2](https://ui.aceternity.com/components)

### Ant Design (`ant-design`)

Data-dense forms, tables, navigation and feedback.

**Find by:** controls, complex-information, layout. **Form:** package, system. **Stack scope:** react.
**Access:** Bilingual AI docs, component Markdown, semantic structure, design docs and MCP links.
**Adoption judgment:** Inspect component semantics and version; other framework implementations have their own contracts.
**Primary sources:** [Source 1](https://ant.design/docs/react/llms/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Apache ECharts (`echarts`)

Charts, visual relationships, interaction and server-rendered graphics.

**Find by:** complex-information, imagery. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** Example editor with code export, APIs and handbook.
**Adoption judgment:** Choose the right representation and renderer; test real data and accessible equivalents.
**Primary sources:** [Source 1](https://echarts.apache.org/handbook/en/basics/import/) · [Source 2](https://echarts.apache.org/handbook/en/best-practices/canvas-vs-svg/) · [Source 3](https://echarts.apache.org/handbook/en/how-to/cross-platform/server/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Base UI (`base-ui`)

Customizable menus, overlays and form interaction foundations.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** react.
**Access:** llms index, APIs/examples and package installation.
**Adoption judgment:** Check controlled state, portals, focus and styling scope; validate accessibility in the composed result.
**Primary sources:** [Source 1](https://base-ui.com/react/overview/quick-start) · [Source 2](https://base-ui.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://base-ui.com/react/overview/quick-start) · [Source 2](https://base-ui.com/llms.txt)

### Codrops (`codrops`)

Creative composition, graphics, interaction and implementation techniques.

**Find by:** design-reference, visual-effects, motion. **Form:** reference, source. **Stack scope:** reference.
**Access:** Search/categories, live demonstrations and tutorial/source pairs.
**Adoption judgment:** Extract transferable mechanisms and assess each example license, dependencies and product fit.
**Primary sources:** [Source 1](https://tympanus.net/codrops/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Embla Carousel (`embla`)

Controlled carousel movement, dragging and slide relationships.

**Find by:** motion, controls. **Form:** package, engine. **Stack scope:** javascript, multi-framework.
**Access:** Examples, parameter guides and framework packages.
**Adoption judgment:** Use a carousel when it serves the content; check focus, touch, autoplay and reduced motion.
**Primary sources:** [Source 1](https://www.embla-carousel.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Finesse UI (`finesse`)

Figma component, variant and page-composition reference.

**Find by:** design-reference, layout, foundations. **Form:** design-file, reference. **Stack scope:** design-tool.
**Access:** Design-kit catalog and Figma entry.
**Adoption judgment:** Treat it as a design file; verify purchase/access and any implementation or asset rights.
**Primary sources:** [Source 1](https://finesseui.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: design-reference; potential scope: page, component-family; forms: design-file-not-runtime-implementation.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://finesseui.com/)

Finesse UI at finesseui.com is a design-kit entry, not mouse-lin/finesse-skill. The latter is a separately attributed method source, not an adopted UI component.

### Floating UI (`floating-ui`)

Floating-element alignment, collision and available-space handling.

**Find by:** controls. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** Live examples, positioning APIs and packages.
**Adoption judgment:** Assign positioning and complete control semantics separately; check scroll containers and layer ownership.
**Primary sources:** [Source 1](https://floating-ui.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Fontsource (`fontsource`)

Self-hosted font families, weights, subsets and variable fonts.

**Find by:** typography. **Form:** font, package. **Stack scope:** framework-neutral.
**Access:** Font catalog, llms index/full docs, page Markdown and font API docs.
**Adoption judgment:** AI docs cover usage and exclude generated font catalog pages. Inspect actual family/glyph coverage and individual font terms separately.
**Primary sources:** [Source 1](https://fontsource.org/docs/getting-started/introduction) · [Source 2](https://fontsource.org/docs/getting-started/ai-and-llms)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### GSAP (`gsap`)

Timelines, scroll, text and coordinated multi-element motion.

**Find by:** motion, typography. **Form:** package, engine. **Stack scope:** javascript, framework-neutral.
**Access:** llms index, core/plugin APIs and examples.
**Adoption judgment:** Check scope, teardown, reduced motion, repeated interaction and applicable license.
**Primary sources:** [Source 1](https://gsap.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: implementation-route; potential scope: effect, timeline; forms: sequencing-engine.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://gsap.com/llms.txt)

### Iconify (`iconify`)

Search and distribute icons across multiple collections.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral.
**Access:** Collection directory, APIs, components and offline icon data.
**Adoption judgment:** Check each collection license and visual fit; choose online retrieval or local bundling deliberately.
**Primary sources:** [Source 1](https://iconify.design/docs/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Inspira UI (`inspira`)

Copyable Vue/Nuxt backgrounds, text, interaction and display components.

**Find by:** visual-effects, motion, layout. **Form:** source, visual-component. **Stack scope:** vue.
**Access:** Category documentation, demos/source and installation guide.
**Adoption judgment:** Match Vue, Tailwind and motion-library versions with the selected component documentation.
**Primary sources:** [Source 1](https://docs.inspira-ui.com/docs/en) · [Source 2](https://docs.inspira-ui.com/docs/en/getting-started/installation)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, cards, visual-interaction.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://inspira-ui.com/docs) · [Source 2](https://inspira-ui.com/docs/getting-started/installation)

### LottieFiles (`lottiefiles`)

Graphic animation, loaders and feedback assets.

**Find by:** motion, imagery. **Form:** asset, engine. **Stack scope:** multi-runtime.
**Access:** Asset catalog, developer docs and framework/player integrations.
**Adoption judgment:** Check asset and player licenses separately; assess payload, renderer support and communicative value.
**Primary sources:** [Source 1](https://lottiefiles.com/developers)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Lucide (`lucide`)

Consistent line icons with framework-specific delivery options.

**Find by:** icons. **Form:** asset, package. **Stack scope:** framework-neutral.
**Access:** Icon catalog, framework guides, SVG and packages.
**Adoption judgment:** Match weight, size and accessible naming; retain an adequate interaction target around a small icon.
**Primary sources:** [Source 1](https://lucide.dev/guide/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Magic UI (`magic-ui`)

Expressive effects, text, backgrounds and display blocks.

**Find by:** visual-effects, motion, layout. **Form:** source, blocks, visual-component. **Stack scope:** react.
**Access:** Component docs, Copy Page and documented MCP entry.
**Adoption judgment:** Identify the particular free component or separately sold template; review behavior and effect intensity in the complete page.
**Primary sources:** [Source 1](https://magicui.design/docs/mcp)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: visual-implementation; potential scope: visual-component, block; forms: border-light, text-motion, background, display-composition.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://magicui.design/docs/components/shine-border)

### Mobbin (`mobbin`)

Product-screen and user-flow observation.

**Find by:** design-reference, layout. **Form:** reference. **Stack scope:** reference.
**Access:** Screen/flow search, visible previews and product records.
**Adoption judgment:** Use task and state relationships as reference; content access and permission to reuse product assets are separate.
**Primary sources:** [Source 1](https://mobbin.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Motion (`motion`)

Transitions, gestures, layout changes and motion control.

**Find by:** motion. **Form:** package, engine. **Stack scope:** react, vue, javascript.
**Access:** Framework-specific docs/examples and separately authorized AI tooling.
**Adoption judgment:** Select APIs by interaction purpose and runtime; distinguish base capabilities from tools requiring additional access.
**Primary sources:** [Source 1](https://motion.dev/docs) · [Source 2](https://motion.dev/docs/ai-kit)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: implementation-route; potential scope: effect, interaction-mechanism; forms: animation-and-input-engine.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://motion.dev/docs/react-drag)

### MUI (`mui`)

Product components, themes and complex-interface foundations.

**Find by:** controls, layout, complex-information. **Form:** package, system. **Stack scope:** react.
**Access:** Component APIs/demos, AI documentation and MCP guide.
**Adoption judgment:** Check the specific package/version and any commercial extension terms.
**Primary sources:** [Source 1](https://mui.com/material-ui/getting-started/mcp/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Nuxt UI (`nuxt-ui`)

Product controls, themes, forms and layouts for Nuxt/Vue.

**Find by:** controls, layout, foundations. **Form:** package, system. **Stack scope:** vue.
**Access:** llms index, per-page Markdown, examples and MCP/Skill documentation links.
**Adoption judgment:** Match the installed version and theme mechanism; documented tools become usable through actual host connections.
**Primary sources:** [Source 1](https://ui.nuxt.com/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Open Props (`open-props`)

Reusable CSS sizes, spacing, colors, shadows and easing.

**Find by:** foundations, motion. **Form:** tokens. **Stack scope:** framework-neutral.
**Access:** Token directory, source and import guidance.
**Adoption judgment:** Map selected values into project semantic roles and one coherent set of scales.
**Primary sources:** [Source 1](https://open-props.style/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Paper Shaders (`paper-shaders`)

Parameterized textures, light, metal and dot-grid surfaces.

**Find by:** visual-effects. **Form:** package, demo. **Stack scope:** react.
**Access:** Live parameters and usage examples; the snapshot inspected React examples.
**Adoption judgment:** Review GPU cost, static equivalents, background pause and foreground contrast. Confirm the particular package and runtime.
**Primary sources:** [Source 1](https://shaders.paper.design/dot-grid) · [Source 2](https://shaders.paper.design/liquid-metal)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Penpot (`penpot`)

Editable design structures, assets and token-to-code mapping.

**Find by:** design-reference, foundations, layout. **Form:** design-file, tool. **Stack scope:** design-tool.
**Access:** Design files, token export, official MCP and API.
**Adoption judgment:** Confirm the active document, read/write scope, permissions and host connection before operating on real files.
**Primary sources:** [Source 1](https://help.penpot.app/mcp/) · [Source 2](https://help.penpot.app/user-guide/design-systems/design-tokens/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Radix Colors (`radix-colors`)

Color scales for surfaces, boundaries, emphasis and text across themes.

**Find by:** foundations. **Form:** tokens, package. **Stack scope:** framework-neutral.
**Access:** Color/use guidance and source/package access.
**Adoption judgment:** Map colors to actual roles and verify contrast in real combinations.
**Primary sources:** [Source 1](https://www.radix-ui.com/colors)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Radix Primitives (`radix-primitives`)

Composable menus, dialogs, selection and focus behavior.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** react.
**Access:** Categorized APIs, examples and interaction/accessibility documentation.
**Adoption judgment:** Preserve semantic/state contracts and map styling into project tokens; confirm package names for the selected version.
**Primary sources:** [Source 1](https://www.radix-ui.com/primitives/docs/overview/introduction)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://www.radix-ui.com/primitives/docs/overview/introduction)

### React Aria (`react-aria`)

Input, collection, form and internationalized interaction capabilities.

**Find by:** controls, complex-information. **Form:** package, primitive. **Stack scope:** react.
**Access:** Component APIs, examples and styling guides.
**Adoption judgment:** Evaluate primitive behavior and the complete page separately; use the correct package and state model.
**Primary sources:** [Source 1](https://react-aria.adobe.com/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://react-aria.adobe.com/)

### React Bits (`react-bits`)

Animated backgrounds, text, interactions and expressive display components.

**Find by:** visual-effects, motion, typography. **Form:** source, demo, visual-component. **Stack scope:** react.
**Access:** Index, category demos, source variants and documented component installation.
**Adoption judgment:** Select exact JS/TS and CSS/Tailwind variants; inspect the actual animation/rendering dependencies and preserve demonstration parameters.
**Primary sources:** [Source 1](https://reactbits.dev/llms.txt)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, card-material, pointer-response.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://reactbits.dev/) · [Source 2](https://reactbits.dev/components/spotlight-card)

### Reka UI (`reka`)

Vue menus, overlays, inputs and focus behavior.

**Find by:** controls. **Form:** package, primitive. **Stack scope:** vue.
**Access:** Component APIs, examples and Markdown documentation entry.
**Adoption judgment:** Compose stable interaction with tailored appearance; confirm controlled state and event wiring.
**Primary sources:** [Source 1](https://reka-ui.com/docs/overview/introduction)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation; potential scope: primitive, component-family; forms: visual-treatment-to-be-selected-in-context.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://reka-ui.com/docs/overview/introduction)

### Rive (`rive`)

Designer-authored state-driven graphics and interactive animation.

**Find by:** motion, imagery. **Form:** asset, engine. **Stack scope:** multi-runtime.
**Access:** Runtime documentation, platform capability guides and animation files.
**Adoption judgment:** Check authoring access, asset rights and selected runtime capability/version separately.
**Primary sources:** [Source 1](https://rive.app/docs/runtimes/getting-started)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### shadcn-vue (`shadcn-vue`)

Editable Vue product components and blocks.

**Find by:** controls, layout. **Form:** source, blocks, registry. **Stack scope:** vue.
**Access:** Component documentation, registry/CLI and MCP guide.
**Adoption judgment:** Select the Vue source, CLI and dependencies explicitly; distribution schema and framework compatibility are separate facts.
**Primary sources:** [Source 1](https://www.shadcn-vue.com/docs/mcp)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation, visual-implementation; potential scope: component, block; forms: coordinated-controls, product-blocks.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://www.shadcn-vue.com/docs/mcp)

### shadcn/ui (`shadcn`)

Product components and blocks delivered as editable source.

**Find by:** controls, layout. **Form:** source, blocks, registry. **Stack scope:** react.
**Access:** llms index, demos/APIs, registry, CLI inspection/preview and MCP docs.
**Adoption judgment:** Inspect files, dependencies and global CSS changes before installation; copied source has local maintenance ownership.
**Primary sources:** [Source 1](https://ui.shadcn.com/llms.txt) · [Source 2](https://ui.shadcn.com/docs/cli) · [Source 3](https://ui.shadcn.com/docs/registry/registry-item-json)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: functional-foundation, visual-implementation; potential scope: component, block; forms: coordinated-controls, product-blocks.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://ui.shadcn.com/llms.txt) · [Source 2](https://ui.shadcn.com/docs/cli) · [Source 3](https://ui.shadcn.com/docs/registry/registry-item-json)

### TanStack Table (`tanstack-table`)

Headless sorting, filtering, columns and table state.

**Find by:** complex-information. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** Framework-adapter docs, APIs and examples.
**Adoption judgment:** Choose behavior and appearance separately; test actual data scale, keyboard behavior and server-query boundaries.
**Primary sources:** [Source 1](https://tanstack.com/table/latest)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Tiptap (`tiptap`)

Extensible rich-text and structured editing.

**Find by:** complex-information. **Form:** package, engine. **Stack scope:** multi-framework.
**Access:** APIs, extension directory, framework guides and examples.
**Adoption judgment:** Check editor state, content format, persistence and extension rights against the real scope.
**Primary sources:** [Source 1](https://tiptap.dev/docs/editor/getting-started/overview)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Uiverse (`uiverse`)

Community examples for buttons, loaders, forms and cards.

**Find by:** controls, visual-effects. **Form:** source, reference. **Stack scope:** html-css, react.
**Access:** Category search, live preview and item code.
**Adoption judgment:** Assess each author/item for semantics, license and maintainability; gallery membership identifies a lead.
**Primary sources:** [Source 1](https://uiverse.io/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### unDraw (`undraw`)

Subject illustrations with adjustable accent color.

**Find by:** imagery. **Form:** asset. **Stack scope:** framework-neutral.
**Access:** Browse/search, color preview and download.
**Adoption judgment:** Check original asset terms for the actual product use and any redistribution/platform integration.
**Primary sources:** [Source 1](https://undraw.co/) · [Source 2](https://undraw.co/license)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Utopia (`utopia`)

Fluid type, space and grid tools.

**Find by:** foundations, typography, layout. **Form:** generator, reference. **Stack scope:** framework-neutral.
**Access:** Generators, method guidance and CSS output.
**Adoption judgment:** Calibrate generated bounds to real content and device conditions; parameters are design choices.
**Primary sources:** [Source 1](https://utopia.fyi/)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

### Vue Bits (`vue-bits`)

Animated backgrounds, text, cards and visual interactions.

**Find by:** visual-effects, motion, layout. **Form:** source, demo, visual-component. **Stack scope:** vue.
**Access:** Category demos, configuration/source, Copy for AI, documented registry/MCP and a source-linked llms index.
**Adoption judgment:** The snapshot located llms.txt in official source; its direct fetch was unavailable. Check the exact MIT + Commons Clause terms and host tool availability for adoption.
**Primary sources:** [Source 1](https://vue-bits.dev/get-started/mcp) · [Source 2](https://vue-bits.dev/text-animations/fold-text) · [Source 3](https://github.com/DavidHDev/vue-bits/blob/3766ebeeed37ec35bce29f001b6d101c7b17da35/src/utils/aiExport.ts) · [Source 4](https://github.com/DavidHDev/vue-bits/blob/main/README.md)
**Evidence:** documentation_or_public_source; reviewed 2026-10-24; project use: evaluate_in_project.

**Craft discovery:** roles: visual-implementation; potential scope: visual-component, effect; forms: background, text-motion, cards, interaction.
**Profile basis:** Documentation role classification; not a visual audit or claim of adoption. Reviewed 2026-10-28. Not rated: exact item, visual completeness and project fit require actual task-time observation.
**Profile sources:** [Source 1](https://vue-bits.dev/)

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
