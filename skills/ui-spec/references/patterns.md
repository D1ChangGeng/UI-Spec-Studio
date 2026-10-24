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

## Preserve a useful technique

When adapting one of these patterns, keep a short record only if it will improve future work: the task, the transferable relationship, local constraints, editable source, inspected evidence and limits. Separate the project's aesthetic choice from the general mechanism. Add new shared patterns through an authorized maintenance change, with provenance and a concrete counterexample that shows where the technique should change.
