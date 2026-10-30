# Source responsibility and retained implementation

This coordinator review examines the frozen applications after their executions.
It is separate from the fresh, anonymized product inspections. It establishes
specific lineage and adaptation facts; it does not infer visual quality from
imports, source-file size or dependency count. See [RESULTS.md](RESULTS.md) for the
product findings, the [registration](registration.json) for the exact methods and
the per-run archive indexes for the actual files.

## Collection workspace: T1

### A — T1-p6

The application actually includes the pinned Magic UI MagicCard implementation.
The radial surface, edge-light calculation, pointer coordinates and reset behavior
survive in the integrated card. Dynamic reduced-motion and coarse-pointer handling
are focused additions. Lucide supplies the icon family; locally supplied Instrument
Serif and DM Sans retain their font licenses. The source notes distinguish these
adoptions from Bootstrap Album, whose demonstration was observed as a reference
but whose page and CSS implementation were not adopted.

The author explicitly identifies page structure and type tokens as project-authored.
The actual page has a custom header, title/count composition, search/filter row,
card grid and reading layout. MagicCard provides meaningful local craft, but does
not account for those page-level decisions. This is a concrete baseline example
of strong local resource use coexisting with independently constructed surrounding
visual relationships. It is not evidence that those relationships are necessarily
poor: the independent product review must judge the visible result separately.

Primary saved explanations: `SOURCES.md`, `DESIGN.md` and `RESULT.md` in the
[participant archive](runs/T1-p6/participant-evidence.zip). Actual source is in
[application.zip](runs/T1-p6/application.zip), including font licenses and the
adopted MagicCard.

### B — T1-n2

The application imports the supplied Bootstrap CSS and the Blog example's CSS,
uses Album's container/row/column/card relationships and independent card actions,
and integrates the pinned MagicCard source. The authored stylesheet configures
Bootstrap's semantic colors, component variables and responsive fit. The selected
Blog serif/sans relationship and system fallback are explicit. The source notes
do not claim to have installed a new font merely because a reference uses one.

This provides a broader actual foundation than A's local component alone. The
card grid, control roles, alert treatment and typography relationship can be traced
to adopted source families. The coordinator inspected the imports, classes,
stylesheet and recorded adaptations, rather than accepting the source table as
proof. No original-work exception was invoked.

The adaptation exposed genuine conflicts: Bootstrap's important border rule
masked MagicCard's transparent edge mechanism; default smooth scrolling interfered
with context restoration. The final source contains targeted fixes for both. A
source's presence therefore did not by itself preserve its value. The author also
adjusted sticky navigation below the actual storage-warning height.

Primary explanation: `DESIGN.md` and `evidence/adopted-sources.json` in the
[participant archive](runs/T1-n2/participant-evidence.zip); actual implementation
and source notices in [application.zip](runs/T1-n2/application.zip).

## Continuous card: T2

Both applications acquired the same licensed Kokonut CardFlip v2 source and
preserved actual mechanisms. They took different integration routes. Treating
one as reuse solely because it retains a longer source file would contradict the
policy under examination.

### A — T2-v9

`app/flip-motion.js` ports the source's substepped spring integration, stiffness
170, damping 20, seven depth slices and angle-dependent lift, shadow and light.
The source's distinctive relationships are recognizable in the math and DOM
realization. Its controller is narrowed to explicit 0/180-degree button turns;
dragging, pointer tilt and arbitrary spins are not claimed as retained capabilities.
The author records that boundary and keeps the MIT attribution.

This is source-derived adaptation, not simply a remembered technique or a
screenshot reconstruction. New vanilla code does not automatically make it
prohibited original construction. Whether the retained mechanisms actually serve
the task remains an independent UI question. The existing storage owner remains
in `app.js`. The port also compensates for the settled face's depth translation,
and synchronizes hidden-face interaction with observed orientation.

The surrounding paper treatment and type choices include author-led adaptation
of the existing fixture. Their quality and provenance should not be conflated
with the clearly identified motion lineage. The current experiment does not
retroactively certify every baseline styling choice against the new policy.

Source and limitations are in `DESIGN.md`, `app/flip-motion.js` and
`app/THIRD_PARTY_NOTICES.md` in the two [run archives](runs/T2-v9/archive-index.json).

### B — T2-k4

The actual component differs from the pinned source in a small, documented set
of responsibilities: localized help/role descriptions and immediately settling
an active turn when reduced motion becomes enabled. The source's spring,
instantaneous angle/velocity, seven thickness layers, depth, perspective,
angle-linked lift/light/shadow and pointer/keyboard interaction remain. A React
island receives the existing front/back content while the vanilla controller
retains storage, saving delay, draft and language ownership.

This is substantive direct adoption with focused adaptation. It is not merely
an imported name. Existing shell/type/color relationships were inspected and
retained; spacing was expanded after sampled intermediate frames revealed the
perspective envelope reaching the heading and actions. The original sample
content is replaced with real note content and a return-to-editor action.

Direct adoption carries costs. It adds a React/Tailwind build to a previously
vanilla task. It also does not establish that text rasterization, motion envelope
or mobile action placement are optimal in this composition. Those are product
inspection questions even when the original mechanism is intact.

Detailed source comparison: `evidence/source-adaptation.diff`,
`DESIGN-RECORD.md`, `app/src/components/card-flip.tsx` and the MIT notice in the
[run archives](runs/T2-k4/archive-index.json).

## Accepted-system increment: T3

The task explicitly accepts the existing layout, palette and editor relationship.
Both applications preserve that foundation, use 14px placeholders with 15px
entered text, retain the existing control proportions, and implement an original
folded-page identity mark within the specifically requested brand position.
These are deliberately different authorities: system inheritance for the type
change and explicit originality permission for the mark.

Both add a native dialog for conflict comparison while inheriting existing color,
type, boundary and button roles. Native dialog supplies semantics, modal focus
and Escape behavior; it does not by itself establish visual maturity. The user
has separately authorized only the missing local comparison presentation if the
existing mechanisms cannot express it. Neither application uses the brand request
as permission to redesign the general page.

B explicitly identifies W1 for the mark and W3 for the necessary comparison.
It inspects the existing status/recent-save regions and a live Bootstrap Modal
example, records that Bootstrap was considered but not adopted, and keeps the
project system as the main foundation. This is evidence of scoped authority and
a concrete local gap; it is not an exhaustive proof that no reusable comparison
implementation exists anywhere. A also examines comparison references and
implements within the task's same narrow permission.

Both keep the future quotation-support representation as research: the actual
record has only title and free text, so neither fabricates quotation identifiers,
support edges or coverage percentages. This protects missing product facts. It
does not separately test the W2 exception or a source-only gap without permission.

Primary records are `evidence/DESIGN.md` / `FUTURE-EVIDENCE.md` for
[T3-r8](runs/T3-r8/archive-index.json), and `notes/DESIGN.md` /
`FUTURE-EVIDENCE.md` for [T3-c7](runs/T3-c7/archive-index.json).

## Engineering and claim boundaries

Build logs are evidence about those builds, not a browser performance benchmark.
The T1 builds both include approximately 399 kB of main JavaScript before gzip;
B's Bootstrap-backed CSS is approximately 254 kB, versus approximately 37 kB in
A's final build. A additionally distributes local display/body fonts. B's source
scope therefore has a real stylesheet cost, with no measured loading-time or
low-end-device conclusion.

T2 B's saved build lists approximately 265 kB of main JavaScript, a 9.6 kB business
chunk and 38.5 kB of CSS; A keeps a static vanilla entry and adds its bounded
motion adapter. These are different maintenance tradeoffs, not a resource-count
score. The shared starter already listed optional dependencies for both conditions;
that list does not establish which dependencies entered a running product.

No coordinator repair was applied to the frozen applications. Source inspection
does not establish user acceptance, universal maturity or compliance of every
possible future action. The decisive product findings and their limits remain
in the independent reports and [study results](RESULTS.md).
