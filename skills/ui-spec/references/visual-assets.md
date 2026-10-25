# Visual assets and asset engineering

Treat visual assets as designed parts of the experience. They can establish identity, explain content, carry a focal point, express material or space, and communicate change. Templates and components organize use; assets supply some of its content and visual substance. Background, type and motion can involve both authored assets and runtime behavior. Their design and engineering decisions work together.

This common reference supplies asset judgment for every round. The actual task determines production depth. The reuse ladder describes scope, not visual importance: a load-bearing photograph, wordmark or spatial object can shape the whole page. Discover suitable assets alongside mature page foundations, and let a strong finding improve the composition. Preserve an asset-light direction when it serves the product.

## Contents

[Role and conditions](#establish-the-role-and-the-viewing-condition) · [Research and selection](#research-compare-and-choose-a-production-route) · [Identity](#brand-and-icon-craft) · [Type](#type-glyphs-and-wordmarks) · [2D](#2d-preparation-and-image-direction) · [Spatial production](#spatial-and-3d-production) · [Dynamic assets](#dynamic-assets-and-procedural-presentation) · [Delivery and acceptance](#engineer-masters-derivatives-and-placements)

## Establish the role and the viewing condition

Name the asset's job, target surface/state, intended perception and the relationship it must preserve with text, components and motion. Classify its meaning as identity, informative content, functional cue, expressive focus or supporting atmosphere; one asset can have different roles in different placements. The role determines alternatives, accessible naming, priority and failure behavior.

Inspect the actual material while layout is still adjustable. Record a useful quality target: recognizable silhouette at its small size, a readable wordmark, a specific material response, a focal subject with space for copy, or a loop whose motion leaves the primary task stable. A resource's subject, crop or illumination can change the required layout; revise both together. Asset preparation continues through iteration and real connection.

## Understand the asset family

| Family | Design work | Preparation and runtime questions |
|---|---|---|
| Brand marks, favicons, app and feature icons | Identity, silhouette, proportion, negative space, optical weight and family consistency | Small-size variants, masks/safe areas, light/dark use, source rights and accessible role |
| Interface and third-party brand icons | Familiar action/status or accurate service identification | Selected library/item/version, visual size versus hit target, official brand rules and semantic name |
| Fonts, glyphs, wordmarks and display lettering | Reading roles, character, spacing, custom outlines and deliberate recognition | Script coverage, shaping, metrics, axes, licenses, editable source and loading/fallback behavior |
| Photography, illustration, vector, texture and background | Content truth, composition, focal point, palette, edges and material | Crop variants, dimensions, alpha/color, delivery format, decoding and source provenance |
| 3D models, spatial graphics, scenes and materials | Geometry, camera, silhouette, scale, light and material as one composition | Editable scene, units, transforms, textures, export fidelity, runtime support and poster/fallback |
| Dynamic assets and procedural visuals | Attention, rhythm, loop, state transitions and spatial continuity | Timeline/state machine, renderer, payload, frames, control, reduced motion and lifecycle |

Use this as a connected classification rather than a demand to include every family. Choose assets by their contribution to this product, including clarity and distinctive character.

## Research, compare and choose a production route

Apply the common sourcing method to exact asset candidates and relevant production examples. Study visible quality, actual files and rights-bearing sources. A moodboard supplies direction; the original asset or author supplies provenance. Record separately what is observed, inferred, usable and accepted.

View references at whole-composition, relationship and detail scales; inspect dynamic candidates across their meaningful cycle or interaction. Extract properties such as line tension, optical center, letter joining, light softness and object continuity into a product-specific brief. Compare material in isolation and beside actual text/controls: a strong asset can change the layout, and the layout can expose an asset's limitation. Third-party service marks retain the owner's approved identity and permitted variations.

Choose direct use, adaptation, composition, technique transfer or original production by design fit, required uniqueness, permissions, available tools and total cost. A mature icon library is a strong starting point for routine controls; a distinctive brand symbol may justify original drawing and refinement. Generative tools can explore concepts or supply a base; inspect the actual output and refine it for the required use. A raster preview proves an image result, while editable curves, geometry, animation or a font require their actual source artifacts.

Before an image transformation, establish the usable input and its authorized scope. Before invoking a specialist tool, inspect the host's available capabilities, project/version and export options. Tool awareness, access to a tool, a successful production run and verified output are separate facts. Use available tools directly when appropriate; otherwise identify the precise production dependency and complete independent design work. Keep private reference material within its authorized destinations. Preserve unrelated files and existing masters.

For identity-changing or otherwise consequential alternatives, show a small, researched set at equivalent sizes, backgrounds and placements. Explain the differences the user can perceive and recommend one. Preserve actual approval scope; routine adjustments proceed under the established direction.

## Brand and icon craft

For functional icons, start with an established family and choose the correct semantic item. Coordinate stroke, fill, apparent weight, baseline and optical size rather than forcing equal bounding boxes. Keep the interaction target usable independently of the drawing's size. Pair unfamiliar symbols with language; name actions at the control. Brand-library availability and permission to use a particular mark are different checks. Consult current owner guidance for service logos, with accurate attribution and relationship claims.

For an original mark, explore silhouette and positive/negative space before adding material or motion. Tune contour, proportion, joins and balance at actual display sizes. Establish a recognizable core that can support a small mark, full lockup and optional expressive treatment. A favicon may need optical simplification rather than a mechanically reduced illustration. App-icon masks and safety regions follow the target platform. Inspect monochrome and inverse uses, dark/light grounds, browser-tab size and larger identity contexts. Screen geometry supports judgment; actual perceived balance decides the refinement.

Identity references teach how a form works. Preserve another brand's identity when representing that brand, and develop an independent expression when creating the current product's mark. Record design approval separately from any legal review of intended use.

## Type, glyphs and wordmarks

Choose mature fonts for the actual languages, text roles, numerals, punctuation and weights. Inspect real mixed-script text and fallback metrics. Check the required subset, shaping, variable axes, readability and loading behavior in the target environment. Font selection includes the license for web/app embedding, modification and distribution; obtain the exact permitted source rather than assuming that a visible font is available for reuse.

Choose limited outline customization or a purpose-made wordmark when identity calls for it. Joining letters, reshaping strokes, abstracting counters or adding depth can create a graphic with a second layer of recognition. Decide whether immediate reading or slower discovery serves its placement. Preserve a clear semantic name and readable ordinary interface text. Keep the text spelling, outlines, spacing and intended lockups reproducible. A wordmark image and a functioning typeface are distinct deliverables; turning outlines into a font additionally needs encoding, metrics, shaping, testing and appropriate rights.

## 2D preparation and image direction

Select or create material at a quality suitable for its largest required use, then derive purpose-specific outputs. Control crop, focal point, negative space, contrast, resolution, alpha and edge quality with the actual neighboring content visible. Use separate compositions when one crop cannot preserve the subject and reading area across viewports. Track light/dark variations intentionally; automatic inversion is suitable only when it preserves the design and allowed identity.

For reconstruction, compositing or vectorization, inspect masks, contour economy, local color, repeated textures and artifacts at delivery size as well as close up. Retain editable layers/paths when later changes need them. Apply an intentional color pipeline; compare exported colors, transparency and gradients in the target browser or host. Preserve factual product representation, and label illustrative substitutes where interpretation depends on it.

Choose SVG for suitable vector forms and supported raster formats for their content, alpha, decoder compatibility and measured visual/byte tradeoff. Inspect SVG before use for scripts, external fetches, embedded data and ID collisions according to the actual trust boundary. Use responsive image sources and intrinsic dimensions so layout remains predictable while files load. Critical imagery gets appropriate loading priority; secondary media can defer. Test the final generated/optimized file, since compression or conversion can alter the intended result.

## Spatial and 3D production

Choose the construction route and delivery mode separately:

| Production route | Useful starting point | Required refinement |
|---|---|---|
| Reuse an existing model or scene | Suitable geometry, material or lighting setup | Rights, proportions, camera, materials and project-specific composition |
| Model and render | Vector paths, sketches, primitives or designed mesh | Topology, bevels, normals, UVs, material, light and camera |
| Procedural/parametric work | Geometry Nodes, Houdini networks or another parameterized process | Meaningful controls, stable seed/evaluation, bounded complexity and reproducible output |
| 2D-to-3D | Clean contour extrusion, layered depth, image-based reconstruction or generated geometry | Depth assumptions, unseen surfaces, silhouette, topology, UVs and material cleanup |
| Hybrid production | Existing/generated base plus modeling, texture and compositing | Consistent scale, light, style, provenance and editable ownership |

A single image constrains visible appearance; hidden geometry remains an inference until supported or deliberately designed. A flattened render can be sufficient for a fixed-view hero, while a rotatable object needs acceptable unseen surfaces and lighting. Inspect the intended views before selecting the export.

Use Blender, Cinema 4D, Spline, Houdini or other available tools for the capabilities the route actually needs. Verify the selected version's format/feature support. Keep the native scene, linked textures, fonts where licensed, node configuration, render settings, camera and meaningful parameters at their authorized project locations.

For **static rendering**, optimize the final image and its responsive crops. For **pre-rendered animation**, check readable frames, loop seam, poster, codec/alpha support and user controls. For **real-time 3D**, preserve usable interaction and content when the renderer is unavailable. Check geometry, draw calls, texture resolution, compressed-texture/mesh decoder support, material/shader compatibility, units, bounds, pivots, orientation, animations and lighting in the target runtime. Re-import or load the exported file rather than assuming the modeling viewport survived conversion. GLB/glTF is a delivery candidate, not a guarantee that every authoring feature exports. A poster-first experience can keep the task usable while heavier resources are prepared.

## Dynamic assets and procedural presentation

Choose CSS/SVG for suitable local state changes, an animation runtime such as Rive or Lottie for compatible authored assets, video for predetermined sequences, and real-time graphics when the interaction or changing scene warrants them. Verify the particular exported features, renderer and dependencies. Connect state-machine inputs and events to actual application state; a loop should not imply progress or success that the system has not established.

Keep readable stable states, intentional loop boundaries, interruption and a quiet alternative. Give prolonged nonessential motion suitable pause/control; honor reduced-motion preferences, offscreen suspension and cleanup. Observe the delivered sequence at its actual placement, including the loop join, maximum reach/brightness and a relevant unavailable state. For nonperiodic effects, choose a window that samples their meaningful variation and state its limits. Use ordered frames to locate a defect and normal-time playback or interaction to judge rhythm; the [temporal verification method](verification.md) keeps observation and capture conditions explicit.

## Engineer masters, derivatives and placements

Maintain a small trace for consequential assets: **purpose and source → editable master → transformation/export → delivery variants → component/host placement → observed result and approval**. Use the project's existing records or [asset record](../assets/templates/asset-record.md). A shared asset ID can link multiple surfaces; a new tracking service is optional rather than inherent to this practice.

Preserve source URL/author/version and applicable terms, allowed changes, required notices and intended publication scope. Keep acquisition rights, trademark guidance, content consent and generated-output provenance distinct. A permissive tool license says little about an arbitrary imported model, font or image. Do not place restricted masters in a public release; ship only outputs authorized for that destination.

Record the relevant derivative properties: dimensions/aspect, intended CSS size and pixel density, format/MIME, theme/crop, color/alpha, byte budget, duration/fps/state names or scene/texture details. Keep export settings, dependency versions, output identity/hash and owner when they matter for reproduction. Point to the current master and let ordinary version control preserve history.

Assess total resource cost: transferred bytes, decode/startup, decoded image/texture memory, rendering work, idle activity, and integration/maintenance. A small compressed file can still expand into a large texture or costly runtime. Choose project-specific budgets and test on representative devices/network conditions; no universal byte or polygon number certifies fit. Coordinate several assets so their cumulative cost and visual weight serve one page.

## Accept the asset in use

Compare the original intention, the delivered file and its actual placement. Inspect intrinsic asset craft and composed page quality separately. Use real size, theme, contrast, density, text and viewports; review at least the intended critical states. A large source preview is useful for editing, while small-size and final-host views establish use quality.

Apply family-specific checks: icon recognition and optical weight; wordmark readability/identity; language and font fallback; crop/alpha/color; model geometry/material/light; loop/state continuity; load failure, motion preference and runtime fallback. Verify accessible meaning according to the asset's role. File dimensions, licenses, byte counts and tests provide engineering evidence; the visual result still needs inspection.

Complete the current asset slice with an inspectable preview, chosen direction, source-to-output mapping, actual checks and precise remaining conditions. When a master or shared asset changes, regenerate its derivatives and inspect affected placements. Finish carries these verified assets into real content and host behavior with their editable sources and ownership intact.

## Source support

The [asset source map](asset-sources.md) links primary material for icon provenance, brand usage, type production, scene exports, animation runtimes, image delivery and accessibility. Follow the exact source relevant to the selected route; its evidence scope remains separate from project validation.
