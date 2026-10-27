# Technique patterns: from a problem to editable form

Read these when a concrete technique helps the current design. They are original reasoning examples with representative content, not measured model-performance claims. Adapt the mechanism to the actual task; the common principles remain the foundation.

## A comparison that makes differences legible

**Problem.** Several options repeat the same attributes, while users must compare values before choosing.

**Mechanism.** Align equivalent attributes, distinguish the primary decision factors and keep units/missing values explicit. A comparison table or coordinated rows exposes differences more directly than separate descriptive cards when cross-reading is central.

**Realization.** Use semantic row/column headers and a content model with stable attribute keys. Keep the selected object identifiable. On a narrow display, choose scoped table scrolling or an attribute-preserving stacked presentation according to the actual reading task. Expose column measures, row spacing and selected emphasis as semantic controls.

**Inspect.** Try unequal labels, missing values, keyboard selection and long translated text. Check whether the same question can be answered in each layout. Distinct objects without comparable properties may need editorial summaries instead.

## Evidence beside a conclusion

**Problem.** A reader can see a claim but must repeatedly leave it to inspect its basis.

**Mechanism.** Pair the claim with a traceable source. A shared selection connects evidence and explanation while maintaining orientation.

**Realization.** Give claims and citations stable identities. A wide view may coordinate reading panes; a narrow view may expand the associated excerpt in document flow. Preserve a return target, scroll context and source permission. Use the same selected-state language in both representations.

**Inspect.** Follow multiple citations, return, handle a restricted or missing source and refresh. The excerpt must actually support the claim. This layout earns its density when evidence inspection is part of the task; short uncomplicated content can remain inline.

## A focused task with balanced presence

**Problem.** A small form feels lost in a large canvas or drops toward its bottom.

**Mechanism.** Treat readable control size and total composition occupancy separately. Group the task and necessary explanation, then balance their mass within the usable frame.

**Realization.** Bound the form measure, preserve a consistent spacing hierarchy and use flexible outer space. Begin with visual centering or a slight upward optical bias for compact tasks. On short viewports, natural content access governs the layout. A page inside an existing family inherits its stable shell.

**Inspect.** Compare whole viewports, long errors, zoom and virtual keyboard conditions. The exact offset is a project decision. Large reading surfaces or activity feeds instead need a stable upper origin and growth below.

## An option change that preserves orientation

**Problem.** A local choice causes an entire section to disappear and re-enter, moving the user's attention away from the control.

**Mechanism.** Preserve anchors and component identity; acknowledge the selection immediately and transition only affected information. Pending data and confirmed data have distinct semantics.

**Realization.** Key components by the represented object, not a changing animation counter. Associate request results with the latest valid intent. Reversible effects begin from the current visual state. Editable controls include response duration, emphasis and which content groups participate, while business state stays authoritative.

**Inspect.** Reverse the selection rapidly, delay or fail a response, use keyboard input and reduce motion. A smooth transition that shows an obsolete result fails the task; correct state and continuous presentation are joint requirements.

## A publication that helps a reader begin

**Problem.** A tool's README contains many features but makes fit, installation and first use hard to find.

**Mechanism.** Order information by the reader's decisions: purpose and fit, immediate entry, working example, deeper model, evidence and maintenance. Use real links and native text for the essential path. A distinctive illustration can make the organizing idea memorable without carrying the only explanation.

**Realization.** Use the publishing host's headings, links, code blocks, disclosure and tables. Design a theme-aware illustration from editable geometry and inspect it at actual display sizes; provide a narrow composition when a wide layout becomes illegible. Keep all necessary claims and commands selectable. The artwork's source, palette roles and build command remain available.

**Inspect.** Read at narrow and wide widths, switch themes, disable images, use keyboard links, copy the command and verify its installed result. A host-compatible local preview and the remote host are separate verification conditions. This repository's README applies this pattern as its own product surface.

## An explanatory diagram with semantic integrity

**Problem.** Prose describes relationships that a reader must mentally reconstruct.

**Mechanism.** Decide whether the relation is sequence, containment, dependency, state or quantity. Choose one dominant visual grammar, use consistent roles and encode direction and boundaries explicitly.

**Realization.** Keep the source entities/edges or data alongside generated SVG/layout code. Route connectors for readability while preserving their endpoints. Use semantic text, units and legends where needed. Offer a readable textual or tabular equivalent. Controls such as node spacing, label measure and emphasis remain separate from the underlying facts.

**Inspect.** Trace a path against the source, check overlaps at actual size and verify color-independent meaning. For a simple list, native prose or a table may be more direct. A visually elegant diagram with incorrect topology is not an acceptable tradeoff.

## Familiar work with an expressive visual language

**Problem.** A professional research tool needs an independent artistic identity while preserving understandable questions, sources and durable results.

**Mechanism.** Separate the familiar task relationship from its visual form. Study conversation and evidence inspection as functional references, then investigate cross-domain type, photography, material or editorial composition. Select a coherent theme and mature implementations that can carry it into working inputs, results and navigation.

**Realization.** Trial defining assets beside actual text and controls before scaling the design. Assign display, reading and control type roles; make crop, surfaces, spacing and motion adjustable. Existing input, focus and state mechanisms can remain while the product's visual relationships change. A theme might connect covers, citations and result sections through proportion or material rather than one repeated decoration. This is one application, not a prescribed editorial style.

**Inspect.** Compare equally resolved directions with representative content. Check populated work, long results, returning to sources, repeated input and a reduced-motion treatment. Record usability and expressive completion independently. If an animated asset competes with input, test its location, local intensity, suspension or delivery; preserve the selected direction where feasible. A simple local repair in an already accepted product can inherit its expression without opening a new art-direction study.

## A faithful source becomes an authored sequence

**Problem.** A selected static composition needs a timed presentation explaining its relationships without losing its visual craft.

**Mechanism.** Preserve the source's meaningful layers, typography, material and spatial relationships; animate a semantic sequence such as evidence connecting to a decision and then to a result. Give important text stable reading intervals and the loop an intentional reset.

**Realization.** Reuse editable source layers and a suitable timeline/runtime. Fix stage, content, assets and relevant seeds; expose timeline positions for repeatable frame comparisons. Preserve a full-quality source view for matched-region fidelity inspection. Identify output format and actual encoded duration separately from the authoring clock.

**Inspect.** View source, keyframes, intermediate states, seam and final playback at useful scale. Differences locate unintended departures; perceived composition and rhythm need visual judgment. This establishes an authored work. A live product additionally needs semantic controls, variable content, user interruption and actual completion authority; its responsiveness cannot be inferred from the deterministic film.

## Preserve a useful technique

When adapting one of these patterns, keep a short record only if it will improve future work: the task, the transferable relationship, local constraints, editable source, inspected evidence and limits. Separate the project's aesthetic choice from the general mechanism. Add new shared patterns through an authorized maintenance change, with provenance and a concrete counterexample that shows where the technique should change.

## A reading card whose surface follows attention

**Problem.** A professional reading library needs character without making text
or the opening action difficult to follow.

**Mechanism.** Compare a light moving across a stable plane with a card rotating
in space. Both can be well-crafted, but only the second moves the text plane and
may shift action targets. The useful distinction is the intended reading relation,
not whether either component is labelled premium.

**Mature implementation route.** Inspect actual surface-light and tilt demos in
visual-component ecosystems such as React Bits, Vue Bits or Magic UI, plus a quiet
incumbent where it is already credible. These are discovery leads, not endorsed
winners. Trial matched long content, action placement, themes and pointer input.
Retain source/configuration when adopting; use a behavior primitive only for a
separate semantic need, not as proof that the visual effect was reused.

**Failure and inspection.** An opaque child surface can hide the adopted light;
fixed card height can clip translated copy; pointer-only feedback can disappear
on touch. Compare original source, local trial and full page, inspect keyboard
focus and quiet motion, then decide which relation actually supports reading.
Do not recreate the source's light equation simply to claim original code.

## A composer that inherits a whole working relationship

**Problem.** An input is keyboard-operable but still lacks a mature conversation
experience when files, multiline text, pending results or errors appear.

**Mechanism.** The composer, attachment previews, primary/secondary actions and
message continuation belong to one task relationship. Isolated textboxes and icons
are useful foundations, not that resolved region.

**Mature implementation route.** Search complete composer/thread blocks and real
product references. Inspect their populated and interrupted states before committing
the shell; distinguish a styled block from its unstyled primitive API. Adopt the
highest useful coherent scope, retaining layout and state mechanisms where suitable,
then connect the product's actual request and attachment owners.

**Failure and inspection.** Check long localized text, attachment failures, keyboard
entry, cancellation, repeated requests, focus and narrow keyboard conditions. A
beautiful send animation cannot establish message delivery. Existing validated
composers can support a narrow copy edit without restarting broad source discovery.

## A sheet that retains its hand-controlled movement

**Problem.** A panel looks polished in a still, but drags lag, short flicks are
ignored or closing also scrolls the background unexpectedly.

**Mechanism.** Ongoing input, axis ownership, edge resistance and release interpretation
are different from an authored entrance. Inspect a mature sheet's direct manipulation
and state contract before choosing a motion route.

**Mature implementation route.** Compare candidate operation with realistic scrolling
content and focus, then adapt tokens and surfaces rather than replacing its gesture
engine. Use the [interaction method](interaction-and-variants.md) to identify the
actual unresolved behavior. Only a demonstrated unmet condition warrants new physics.

**Failure and inspection.** Test pause-then-release, slow movement, a late flick,
rapid reversal, cancellation and reduced motion. No fixed velocity or spring value
is a universal craft requirement; the intended task and measured use determine fit.
