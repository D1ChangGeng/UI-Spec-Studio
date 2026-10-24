# Finish: carry the accepted experience into real behavior

Read this reference for finish and whenever a design depends on actual data, authority, persistence or consequential business rules. Apply the common analysis and visual principles throughout. Real content and asynchronous states continue to be design work.

## 1. Reconcile the accepted scope with the actual system

Identify the routes, states, interactions and shared rules the user approved. Use approval already supplied in context and relate it to a reproducible source reference, content and captures. Read current implementation, existing APIs, business rules, tests and runtime configuration.

Classify each required capability as reusable, adaptable, missing or dependent on an external resource. Identify the difference between fixture behavior and real behavior. Keep this mapping proportional to the scope; a brief action-to-owner table is often enough.

Determine actual product maturity. In an unreleased build, evolve current code and data models in place, with reproducible initialization and fixtures. In an operating product, derive data, availability and compatibility work from its evidenced obligations. Git provides source history. Operational artifacts serve the system that actually exists.

## 2. Establish the behavior contract

Trace each meaningful action:

`Visible control → UI intent/state → application action → trusted owner → persisted or computed result → feedback and recovery`

Identify inputs, outputs, identity, permission, validation, error meaning and retained context. Reuse authoritative project contracts and establish missing rules at their actual owner. Resolve consequential business questions from reliable sources or explicit decisions; continue independent work while a material decision is pending.

Presentational components render data and emit intent. Application state/adapters coordinate requests, cancellation, synchronization and user continuity. Trusted services enforce protected decisions such as access, object ownership, financial values, inventory, entitlements and workflow authority. A local/offline product uses the local ownership and persistence its architecture requires.

Different entry paths to one task should resolve to the same business meaning and authoritative state. Reconcile duplicate UI state at the correct boundary. A client-side disabled button is feedback; the authorized owner enforces whether the action can happen.

## 3. Sequence complete user outcomes

Choose vertical slices that reach observable real results. Connect the most valuable path and its required dependencies first; follow with related states and supporting surfaces. Consider which missing contracts could change the accepted experience before connecting many dependent pages.

For each slice, know the accepted UI, existing reusable capability, required change, external dependency and verification target. Prefer the current architecture and smallest coherent extension. A static site may need real content and routing; a server-backed workflow may need API, authority and persistence; choose the actual boundary.

## 4. Connect in the current implementation

Reuse approved components behind fixture and real adapters where practical. Maintain deterministic stories or fixture states for visual regression. Keep preview facilities in the development boundary and real actions in the product boundary.

Complete loading, validation, empty content, denied access, concurrency, pending requests, cancellation, retry, duplicate actions, expiration, refresh and interruption recovery according to task relevance. Match response handling to the latest valid intent. For optimistic interactions, reconcile the result and explain recovery when the authoritative state differs.

For consequential side effects, enforce applicable idempotency and authorization at the trusted owner. Treat credentials, private content, output rendering, logging and caches according to the project's security boundaries. Keep user feedback aligned with actual results.

Use real content lengths and errors to refine layout within the accepted system. A materially changed task, appearance or user commitment returns only the affected scope for review. Maintain stable anchors and meaningful focus/input/selection during data updates.

## 5. Verify design and behavior together

**Design track:** compare approved and integrated states with equivalent content, viewport, fonts, theme, locale and animation state. Inspect the whole frame, shared anchors, internal scrolling, responsive behavior and transitions. Preserve the reference conditions and document intentional differences.

**Product track:** execute the actual UI path, observe the authority/persistence result, then verify feedback and recovery. Check relevant permissions, failure/retry, repeat actions, refresh and direct entry. Evidence should connect the visible action to the real result.

Fixture checks establish design behavior. Mocked boundary checks establish the exercised contract. Real integration checks establish the specific environment and actions executed. Record these distinctions alongside pending external validation. Recheck related components when a common cause is repaired.

## 6. Deliver the completed scope accurately

Provide working entry/run instructions, actual configuration boundaries, implemented changes, verification evidence and precise remaining dependencies. Keep design approval, connection, verification and release as separate facts for each scope.

A request to finish authorizes the scoped implementation. Production operations, real payments, publication and third-party account actions use the user's applicable authorization and host controls. Existing authorization can be reused for its stated scope.

Complete independent work while credentials or external services are pending. Describe the next required resource and the behavior it will verify. Final handover states what is working and observed, so the next developer can continue directly from the current source and evidence.

## Preserve design intent at four boundaries

| Fidelity | What to preserve in real integration | Example verification |
|---|---|---|
| Meaning | Content roles, terminology, provenance, user commitments and honest state | Real values and errors express the same task meaning as the accepted design |
| Structure | Information grouping, reading order, stable anchors and task-local paths | Variable content and permissions retain coherent relationships |
| Visual | Type roles, proportions, image treatment, hierarchy and supported variants | Equivalent states match intent and real extremes stay readable |
| Behavior and timing | User control, focus/selection, response ownership and attention sequence | Slow, failed, repeated and out-of-order actions preserve correct feedback |

Identify the relationships that carry the concept, then expose them through semantic tokens, content fields, component variants and state/timing logic. Preserve these controls when replacing fixtures. A decorative rebuild is unnecessary when approved components can render the real states.

For a static publication, connect the actual links, install instructions, source assets and publishing path. For a diagram, connect the real data/relationships and reproducible export. For timed media, preserve source timing and inspect encoded output. These are real delivery boundaries even when a backend is not part of the artifact.

A precise handover explains what can be adjusted, where the authoritative content/state lives, which conditions were inspected and what remains external. Keep high-quality source editable so future refinement improves the existing design rather than reconstructing it from pixels.

## Carry adopted resources through the real boundary

Reconcile each consequential external item with its exact source, version/variant, local adaptation and ownership. Reuse approved resources while their conditions hold. Check actual dependency/CSS impact, SSR or hydration where relevant, lifecycle cleanup, content growth and the data adapter. Source copies retain local maintenance responsibility; package updates follow their version and compatibility contracts.

Map demo callbacks and sample data to real application intent and trusted outcomes. Protected prices, permissions, entitlements and workflow decisions remain with their authoritative owners. Preserve the selected visual mechanism while real loading, denied actions and failures become meaningful states. Validate the combination at representative scale as well as each item independently.

Keep license notices, asset permission and reproducible configuration with the resulting source. Capture integration evidence in project records and propose reusable lessons through authorized maintenance. Final connection quality is the actual product's behavior and appearance, supported by its observed conditions.

## Carry the selected product model and its decision record

Read the accepted model, primary action/result loop, retained context and scoped resource map with the approved SPEC. Preserve business contracts inherited from the existing project while connecting the presentation chosen for the new target. Reuse local visual code because its fit is documented or accepted, and preserve unrelated work.

Resolve every consequential selection row to its real component/data adapter and visible state. Check that resumed work, pending results, permission boundaries and durable outcomes still match the agreed experience. When an engineering constraint changes the product model or key interaction, explain the affected tradeoff and return that decision to the appropriate owner. Keep unaffected integration moving.

Handover includes the current preview, design/resource map, actual approval source, connected task outcomes and observed conditions. The next developer can then distinguish a studied reference, adopted implementation and accepted product result.
