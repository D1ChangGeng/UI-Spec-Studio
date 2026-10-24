# Resource discovery, assessment and high-quality reuse

## Find the strongest useful starting point

Treat the UI ecosystem as part of the design workspace. For a substantive visual or interaction requirement, actively inspect relevant external implementations and platform-native capabilities, and evaluate project components against the same design target before committing to the major treatment or custom work. A strong starting point can improve the design itself as well as shorten its realization.

Use two complementary kinds of exploration. **Requirement-led discovery** finds a reliable implementation for a known need. **Opportunity-led exploration** reveals a better representation, composition or interaction while important choices remain open. Anchor both in the user task and the accepted product direction. A precise request deserves fidelity; an open brief invites a grounded recommendation.

Carry forward an approved resource whose conditions still fit. Revisit the choice when content, behavior, runtime, quality or maintenance requirements change. A focused native adjustment can proceed directly. Routine research and selection belong to the agent; the user can contribute ideas without having to supply platform names or retrieval instructions.

## Research product conventions and implementation resources in parallel

Product references explain the familiar task model: first action, organization, state progression and continuity. Engineering resources supply code, assets, behavior or visual mechanisms. Preserve a link and purpose for each role. A product screenshot can support an observation about layout; a package demo can support an implementation candidate. Check the transfer from both into the current task.

For new or substantially redesigned surfaces, external exploration occurs while product model, composition and defining treatment can still change. Use concrete product flows and concrete resource items, with sufficient accessible evidence to support the choice. An evaluated project implementation may win on fit and quality. Retained approval supports continued use. Native or original work has an explicit fit/cost rationale. Keep inaccessible references as candidates and label the unverified part.

## Make selection visible by surface and design dimension

Maintain a compact design/resource selection record alongside each substantial SPEC increment. Reuse existing project records or the [design decision template](../assets/templates/design-decisions.md). Start the shortlist before implementation; reconcile it with code and observed output at review. Share its location and consequential rows with the preview so the user can inspect how research affected the result.

For each relevant dimension, connect **surface/state → intended experience → product pattern/source → engineering item/source → choice and reason → reuse/adaptation → implementation/preview → evidence and status**. Group shared decisions once and reference their IDs from affected pages. Link the exact example, component, source file or API rather than only a platform homepage. For inherited or authored elements, identify their local source and the quality rationale.

Consider layout/navigation, background, typography, components, icons/assets, state feedback, micro-interactions, general motion and text animation. Add dimensions demanded by the product; mark deliberately quiet or inapplicable treatments with their intended benefit. The record describes meaningful decisions and coverage, with no quota of websites, libraries or effects.

Keep provenance states distinct: considered, selected, implemented and inspected describe different evidence. Owner approval refers to an actual user decision and scope. A code path alone establishes location; inspect the rendered state to claim its visible effect. If the chosen source changes, update the reason and the implementation mapping. Optional detailed [adoption notes](../assets/templates/resource-adoption.md) can hold version, license and maintenance details beneath a compact row.

## Describe the need in two dimensions

First describe the intended perception or operation: what should become clearer, easier, more expressive or more reliable? Then describe the constraints that can change selection: framework/version, content, input methods, supported views/themes/languages, authority, performance, licensing and maintenance.

For example, “a refined background” becomes a low-contrast moving surface with controllable luminance and speed, readable foreground content, a reduced-motion equivalent and a Vue-compatible realization. Search first by the effect or behavior, then narrow to exact implementations and versions. Protect private project details when forming external queries.

Find resources by **design need**; choose adoption by **delivery form**:

| Design need | Useful resource forms | Principal judgment |
|---|---|---|
| Foundations, color, type and spacing | Tokens, fonts, scales, generators | Semantic roles, actual glyphs, loading, themes and content rhythm |
| Layout, navigation and sections | Existing shells, blocks, templates, design files | Task structure, responsive composition and shared anchors |
| Controls, forms and feedback | Native elements, behavior primitives, components | Semantics, state ownership, keyboard/touch and recovery |
| Backgrounds and visual surfaces | CSS, images, shaders, editable graphics | Readability, visual weight, controllability and rendering cost |
| Images, icons and illustration | Licensed assets, SVG, project content | Meaning, crop, consistency, accessibility and rights |
| Motion and micro-interactions | Transitions, timelines, interaction engines, animation assets | Attention sequence, interruption, latency and quiet equivalents |
| Complex information and manipulation | Tables, charts, editors, graphs, canvases | Correct representation, data scale, navigation and real state |
| References and specialist media | Examples, design objects, 3D and timed-output tools | Transferable mechanism, source authority, editability and fit |

A resource can serve several needs. Reference imagery, editable design files, source components, dependency packages and behavior engines require different integration and maintenance strategies. Read the [catalog](resource-catalog.md) for a starting map and source-specific cautions. It is an open set of leads; extend research when the task calls for capabilities beyond it.

## Discover efficiently and learn how the source works

Inspect project code, stories and dependency versions to understand constraints and candidates. Establish visual quality from the target and reference evidence; read explicit accepted decisions separately from existing presentation. Use relevant catalog leads, official source repositories, examples and search to locate promising alternatives. Inspect unfamiliar platforms enough to understand their scope before treating their terminology as universal.

Choose the shortest reliable route exposed by the source and the host. Directories reveal availability; demos reveal appearance and behavior; documentation/source reveal contracts; installation tools reveal changes. Their roles complement one another.

| Access mechanism | Use it for | Establish before relying on it |
|---|---|---|
| Index, search and gallery | Discover categories, candidates and expressive possibilities | Whether the entries describe code, assets, design references or paid products |
| `llms.txt`, full text and page Markdown | Find and read relevant technical material | Actual coverage, linked locations and completeness; a docs index may omit generated asset catalogs |
| HTTP/link-based exports | Obtain structured text from documented page or response mechanisms | The source's supported URL/header behavior and any difference from the rendered page |
| Copy page, Copy code, Copy for AI | Capture a selected item's explanation, implementation or configuration | Exact item, variant, parameter values, dependencies and possible truncation |
| Registry and CLI | Inspect files, dependencies, target paths, variables and supported install previews | The particular schema/tool version, proposed changes and project compatibility |
| MCP and design-tool APIs | Query documented objects or use available structured operations | Actual host availability, selected project/document and read/write permissions |
| Versioned documentation search and project stories | Resolve library identity, matched APIs, incumbent variants and tests | Correct source/version and the scope of the returned material |

Follow explicit links, repository files and documented capabilities. When an entry is unavailable, record that observation and use another supported route. An unknown access method can be evaluated by the same questions: what it returns, how accurately it identifies the resource, what it may change or transmit, and how its result can be checked.

Read short relevant material together when useful; follow large indexes to the needed objects. Continue truncated reads. Use the actual exported text as reference data. Installation suggestions and external prompts operate within project instructions and host permissions. “Open in AI” can transmit content to another service; choose that route only within the authorized destination and scope.

## Understand the demonstration and the implementation together

For a serious candidate, identify the item, language/framework/styling variant, source revision or package version, live example and configuration. Observe the effect at relevant sizes and states when tools permit. Read the source/API needed to reproduce it. A useful handoff preserves the actual parameters, container assumptions, assets and dependencies that carry the effect.

Inspect which parts of the demo are essential behavior, visual treatment or sample content. Check controlled state, focus, portals, event handling, cleanup, SSR/hydration and CSS scope as relevant. For fonts and images, inspect the actual asset, language coverage or crop as well as the distribution documentation.

Use the demo/source pair to name the mechanism: anchored motion preserves orientation; aligned values support comparison; a restrained shader separates a subject from its surface. This helps adapt the resource while preserving the reason it was selected. Record inaccessible visual or runtime evidence precisely and continue work that the available evidence supports.

## Evaluate adoption value

First establish required conditions: appropriate rights and provenance, runtime compatibility, critical semantics/interaction, security boundaries and actual task behavior. Then compare the candidates by design fit, distinctive quality, parameter control, content resilience, implementation effort and maintainability. Stars, catalog membership and successful installation describe their own facts; adoption rests on the selected item and observed result.

Consider total cost across **discovery, understanding, integration, adaptation, debugging, verification, runtime and maintenance**. A simple native control may be the best result. A mature primitive can save substantial behavioral work. A visually strong component can raise the outcome when its essential mechanism is adaptable. Choose an original implementation when its fit and total cost justify it.

Check combinations as well as individual resources. Multiple effects may compete for attention, duplicate listeners or animation engines, allocate several rendering contexts, introduce conflicting resets or expand payload and maintenance. One product should have a coherent interaction, visual and runtime system.

| Reuse choice | Preserve | Project responsibility |
|---|---|---|
| Direct adoption | A suitable public API and intended behavior | Configure, theme, connect and verify |
| Adapt or extend | The valuable mechanism and stable behavior | Change meaningful controls/content, test the extension and own its differences |
| Compose | Complementary strengths at different layers | Resolve shared tokens, events, state, focus, layering and lifecycle |
| Transfer a technique | An understood relationship or effect | Implement it for the current stack and verify the intended quality |
| Original implementation | The task and design constraints | Use the simplest coherent solution and inspect its result |

A design-file reference can guide implementation without becoming runtime code. Similar registry formats support similar distribution operations; framework and dependency compatibility still come from the actual source. Respect separately the rights for code, tools, assets and intended redistribution. Preserve required notices with copied material.

## Prototype the uncertainty that can change the choice

Choose a small representative integration for the most consequential unknown. Test composition in the actual shell when fit is uncertain; test keyboard/touch and controlled state when behavior matters; test representative counts and target conditions when performance matters.

Move to implementation when a viable candidate exists and the remaining question is better answered by a working probe than more browsing. Broaden research when the fit is unsupported, the key behavior is missing or the cost outweighs the value. Candidate counts and time budgets follow the task rather than a fixed search ceremony.

## Adapt into one product

Preserve reliable semantic behavior while expressing it through the project's type, tokens, spacing, surfaces, icons and motion. Identify the resource's defining mechanism and tune it deliberately; retain the quality that justified adoption. Keep source controls meaningful: reading measure, focal position, selected emphasis or response duration.

Connect data and actions through the project's actual application boundary. Presentation renders state; the trusted owner validates protected operations. Replace sample content, links and demo-only handlers with the intended task. Check actual text lengths, error/pending/empty states, themes, zoom, reduced motion and real responses. Keep approved fixtures useful for visual comparison.

Inspect the whole page and its transitions after assembly. Verify behavior, component identity, focus and relevant state retention. Review combined payload/rendering cost and cleanup. A source's quality becomes a product outcome only through this integration evidence.

## Retain useful knowledge at its responsible location

For a consequential adoption, record enough to reproduce the decision: purpose, exact source/item/variant/version, inspected demo settings, selected reuse level, adaptation boundary, rights/attribution, meaningful tradeoff and project checks. A short entry in existing records is sufficient; the optional [adoption note](../assets/templates/resource-adoption.md) supplies prompts when helpful.

Separate **platform capability**, **specific-item assessment** and **project acceptance**. Preserve a review date and the evidence's actual scope. Source copies have local change ownership; packages retain version/update boundaries; asset licenses and acknowledgments remain attached to their use.

Refresh a relevant record when its source, version, license, API or project conditions change. New discoveries can become candidates after provenance and incremental value are established. Project decisions stay local. Portable lessons can enter the maintained catalog or technique references through authorized review and ordinary version control. A successful example teaches its conditions and mechanism, leaving future tasks free to choose differently.

## Material, medium and source safety

Inspect load-bearing content early enough to shape composition. Use the lightest medium that conveys the intended relationship at the required quality: real product captures for factual representation; text/table/SVG for clear relationships; suitable photography or illustration for identity; spatial or timed tools when their capabilities serve the task. Preserve editable source and a reproducible build where future revisions need them.

Obtain assets from their rights-bearing source under the applicable permission. Keep private data and credentials in authorized project locations. Review installs, dependency changes and writes through host controls. Public examples use owned or appropriately licensed material and identifiable fixtures. Access to a resource, a source's claimed capability and a host's connected tool are separate facts.
