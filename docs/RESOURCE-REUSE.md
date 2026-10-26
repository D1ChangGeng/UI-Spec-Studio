# Discover, assess and reuse excellent UI work

Resource discovery serves [product experience alignment](PRODUCT-ALIGNMENT.md). The agent identifies the intended visual and interaction maturity, finds implementations capable of carrying it, trials consequential choices and preserves their value through adaptation. It supplies references for an open functional brief and expands a named reference into concrete experience questions. The result develops the current product's own expression.

## The working relationship

**Target quality → paired reference/resource research → local trial → controlled adaptation → integrated verification.**

Requirement-led search finds an implementation for a known need. Opportunity-led
exploration finds a better expression while meaningful design choices remain
open. Both use the project's task, accepted direction and actual constraints.
Existing suitable choices carry forward. Search terms evolve with the research: task and user intent, interaction pattern, component role, visual relationship and implementation constraints. A newly discovered resource can also reveal a better product direction.

Design references establish relationships worth inheriting; implementation resources carry those relationships into the product. Research them together while the solution is still open. A promising block can improve the proposed layout; an observed interaction can refine the search for a suitable implementation. Inspect actual demos and relevant states. A paired workspace may require resizing, focus movement and return behavior as well as a convincing still image. Keep the carrier and observed subject clear when a showcase embeds another product or artwork.

Judge maturity through the qualities the task needs: readable type, optical alignment, coherent material, discernible states, stable content growth and understandable transitions. Compare corresponding tasks, content and conditions. A candidate with a different appearance may preserve these relationships more effectively. Keep visual judgment, functional correctness, accessibility and runtime performance supported by their respective evidence.

## Use the included resource map

The [readable catalog](../skills/ui-spec/references/resource-catalog.md) provides
37 candidates and seven access mechanisms from the accepted research. Its
[structured data](../skills/ui-spec/assets/resource-catalog.json) is the maintained
source. It retains original research dates and evidence scope. The map is a
starting point for discovery; the exact item and project require their own review.

```bash
python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json
python <skill-dir>/scripts/find_resources.py --need controls --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
python <skill-dir>/scripts/find_resources.py --list-filters
```

Queries match every whitespace-separated term; filters combine. Results are
alphabetical. Stack filtering includes framework-neutral candidates, while
multi-framework adapters need explicit documentation checks. Zero results means
the bundled map has no match, not that the ecosystem has no solution. The helper
is local and read-only; it neither installs resources nor calls external services.

## Use mature implementation as the default

For general UI, prefer adopting, configuring, composing and extending existing
implementations. Begin at the highest appropriate level: page/application
template, design system, layout, functional block, component, icon, font, visual
asset or motion. A coherent foundation can preserve connected proportions,
hierarchy, states and interaction decisions. Add complementary resources for
specific remaining needs. Assess existing repository UI by the same target and
fit criteria; preserve accepted work while its conditions hold.

Actual reuse can take the form of a package, licensed source, exported asset or
port of an existing implementation. Data adapters, state mapping, theme settings
and composition code support adoption. Record design-method transfer separately
when no implementation is carried forward. Choose among candidates by visual
quality, required behavior, compatibility, rights and the total cost through
verification and maintenance.

Custom implementation addresses an identified gap: relevant candidates fail a
necessary behavior or local trial, their adaptation would remove the value sought,
their terms prevent adoption, or the task needs a distinct interaction. First
consider extending a mature foundation and limit new UI mechanisms to the gap.
Perceived coding speed, visual simplicity or understanding the reference is not
sufficient reason to replace a suitable implementation. Independent brand and
artistic assets can use professional custom production with their own quality checks.

## Trial consequential choices before broad integration

Keep four observations connected, with each supporting its own conclusion:

| Object | What to establish |
|---|---|
| Relevant part of the design reference | Which qualities and relationships the current product needs |
| Candidate's original demo | What the resource itself renders and how its relevant states behave |
| Local trial in the current project | Whether those qualities survive real content, font, theme, container and state integration |
| Assembled interface and journey | Whether selected parts form a coherent experience through actual use |

Identify the exact variant/version, demonstration settings, source/dependencies
and intended project changes. For consequential structures, components, assets
and motion, build the smallest running trial that can expose a mismatch before
expanding integration. Use the product's relevant language, long or multiline
content, variable labels, unavailable media, loading/error states and display
conditions. Routine members of a verified system can inherit checks within the
same conditions.

Inspect detail and whole composition. For changing UI, observe the trigger, first
feedback, progression and settled state, plus useful reverse, repeated or
interrupted actions. Apply this to the reference, candidate and local trial as
needed. Captured media, actually viewed intervals and sufficient support for a
motion judgment remain separate facts. A successful trial supplies a foundation
for assembly; the assembled product still receives its own review.

## Adapt while retaining the reason for adoption

Start with content, theme, public configuration and composition. Change internal
structure or behavior where an observed gap requires it. For a material change,
identify its purpose, affected relationships and states to inspect again. A font
change can alter wrapping and control size; a color change can affect boundaries
and focus; an asynchronous integration can change the meaning of feedback.

Compare the adapted result with the original demo and accepted trial at useful
scale, equivalent content and corresponding interaction stages. Preserve the
mechanism that earned adoption and the behavior that makes the task reliable.
Broad changes to layout, state or motion require verification of that changed
scope; upstream maturity supports the starting point, while current evidence
establishes the adapted version's quality.

When assembly exposes a quality gap, choose the repair layer deliberately:

| Observed cause | Useful next action |
|---|---|
| Resource cannot meet a key requirement | Reopen selection and trial a better candidate |
| Adaptation damaged a useful relationship | Isolate the change, recover the relationship and recheck |
| Real content exposes a structural gap | Revisit content organization, component choice and space together |
| Selected resources conflict | Reconcile density, type, material, motion and state logic under the product's design language |
| Reference target does not fit the task | Revisit product intent and the intended experience |

If the target remains unreachable under current constraints, show the actual gap,
its impact and viable paths. A necessary scope or direction change is an explicit
decision; completed integration does not itself change the quality target.

## Read platform mechanisms by responsibility

Indexes and galleries show possibilities. AI text and APIs explain contracts.
Copy/export may preserve the chosen demo settings. Registries and inspection CLIs
expose files, dependencies and supported changes. MCP may provide queries or real
writes; its availability and permissions come from the host. Project stories
supply incumbent components and states. Use the shortest reliable available route.

The [common reference](../skills/ui-spec/references/component-sourcing.md) explains
these mechanisms and their boundaries. Follow documented links and observe actual
results. When an important source requires normal account access, an official
client or an authorized download, first use available evidence and legitimate
alternatives, then ask for the specific assistance that fills the remaining gap.
Group the request around the source, action, required states or interval, and the
decision it supports: for example, a full open-and-close recording or an authorized
resource export. The agent continues comparison and selection after receiving it.
Research access and rights to integrate an asset are separate conditions.

## Keep useful records lightweight

For an important composition, show its role, target quality, source/item/version,
actual implementation location, preserved relationships, adaptations, rights,
observed checks and maintenance responsibility. Distinguish resources researched,
shortlisted, trialled and actually adopted. Reconcile the record with code and the
rendered result: the main structure, core interaction and high-impact detail
should have an appropriate verified foundation. Dependency counts and code shares
alone do not establish that relationship. Existing component/design records are
preferred. The optional
[adoption note](../skills/ui-spec/assets/templates/resource-adoption.md) is available
when a project needs a starting structure.

Show consequential choices beside the working SPEC using the
[decision template](../skills/ui-spec/assets/templates/design-decisions.md) or
existing project documentation. Shared records can serve a page family; detailed
version/license information can stay in adoption notes. See the
[worked study](../examples/product-intent/README.md) for its stated adoption and
verification scope.

Converge when important quality requirements have evidence, consequential choices
have passed their local trials, relevant states have been observed and the
adaptation path is clear. Continue searching where it could change selection,
resolve a major gap or avoid substantial rework. If candidates remain unsuitable,
keep their actual shortcomings and options visible, then choose further research,
targeted assistance, a bounded plan adjustment or limited custom implementation.
Platform documentation, item inspection and project acceptance remain separate.
Successful project-specific choices stay in that project. Portable findings can
enter the shared catalog through authorized maintenance and ordinary version
control. Add a new candidate when its source is credible and it supplies meaningful
coverage or a better fit; refresh relevant records when conditions change.

## Worked decision paths

| Situation | Useful path | Completion evidence |
|---|---|---|
| Existing approved menu still fits | Reuse it; inspect only changed conditions | Affected controls and actual states |
| New Vue account entry | Trial a fitting complete block or coherent behavior/visual foundation; read exact contracts | Local states, keyboard, touch, dismissal, theme and real session results |
| Open visual direction | Inspect a small set of promising mechanisms; recommend and prototype | Whole-frame effect, readability, controls and combined cost |
| Font discovery | Use family catalog for glyphs; AI docs for usage | Real text, variants, loading and licensing |
| Cross-stack reference | Compare native mature implementations and feasible ports before a custom gap | Actual inherited mechanism, current stack behavior and intended visual quality |
| Paid or unavailable resource | Request a specific authorized export or observation when it changes selection; compare viable alternatives | Actual inspection, adoption rights, remaining conditions and independent progress |
| Finish with real responses | Reconcile source state and application authority | Visual and business regression, including delayed/error states |

These are reasoning examples. Executed helper, document-access and publication
checks are described in [the release review](REVIEW-v1.3.0.md) and CI logs.

## Maintain the catalog

Edit the structured data, preserving provenance and observation scope, then run:

```bash
python tools/catalog_docs.py
python tools/catalog_docs.py --check
python -m unittest discover -s tests -v
```

The readable map is generated from this data. CI checks schema, map consistency,
installed access, deterministic queries and self-contained distribution. No
catalog-wide install or quality claim is inferred from those checks.

## Learn content patterns from mature products

Examine headings, navigation language, input labels, decision-time information and state feedback in a comparable real task. Adopt useful content relationships and conventions at their appropriate scope. Current product facts, legal wording, permissions and brand Voice retain their own authority. Link substantial selections to actual strings, components and observed states. The [content method](../skills/ui-spec/references/content-design.md) supports these decisions.
