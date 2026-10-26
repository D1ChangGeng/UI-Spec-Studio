# Finish: carry the accepted experience into real behavior

Read this reference for finish and whenever a design depends on actual data, authority, persistence or consequential business rules. Apply the common analysis and visual principles throughout. Real content and asynchronous states continue to be design work.

## Contents

- [Reconcile the scope](#1-reconcile-the-accepted-scope-with-the-actual-system)
- [Establish the contract](#2-establish-the-behavior-contract)
- [Sequence and connect outcomes](#3-sequence-complete-user-outcomes)
- [Verify and deliver](#5-verify-design-and-behavior-together)
- [Preserve design and resource decisions](#preserve-design-intent-at-four-boundaries)
- [Connect assets and content](#carry-asset-sources-and-delivery-through-finish)
- [Prepare data with correct authority and lifetime](#prepare-data-with-correct-authority-and-lifetime)
- [Support content maintenance and operational work](#support-content-maintenance-and-operational-work)

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

**Design track:** re-answer the reference research questions in the connected product: does the task entry remain available, reading clear and state change understandable? Compare approved and integrated views with comparable content density, scale, fonts, theme and locale. Inspect whole frames and continuous episodes through waiting, result arrival, interruption and return. Align by task event/state; real latency may differ from a demo. Preserve shared anchors, scrolling and object identity, recording conditions and intentional differences.

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

Reconcile each consequential adopted item with its exact source, version/variant, local trial, preserved mechanisms, modifications and ownership. Retain proven resources while conditions hold; replace fixture adapters without rebuilding their effective UI. Check actual dependency/CSS impact, SSR or hydration where relevant, cleanup, content growth and real data states. Source copies retain local maintenance responsibility; package updates follow their compatibility contracts.

Map demo callbacks and sample data to real intent and trusted outcomes. Protected prices, permissions, entitlements and workflow decisions remain with their authorities. Recheck the affected visual/state relationships under real loading, denial and failure. A substantial rewrite of the original layout, state or motion mechanism needs validation of that new responsibility. Validate components and the integrated journey separately; diagnose a quality gap at its source rather than silently changing the accepted target.

Keep license notices, asset permission and reproducible configuration with the resulting source. Capture integration evidence in project records and propose reusable lessons through authorized maintenance. Final connection quality is the actual product's behavior and appearance, supported by its observed conditions.

## Carry the selected product model and its decision record

Read the accepted model, primary action/result loop, retained context and scoped resource map with the approved SPEC. Preserve business contracts inherited from the existing project while connecting the presentation chosen for the new target. Reuse local visual code because its fit is documented or accepted, and preserve unrelated work.

Resolve consequential decisions from the studied relationship through the selected implementation resource and adaptation to the real component/adapter and visible state. Check resumed work, pending results, permissions and durable outcomes against the experience target. When runtime constraints change the model or key interaction, reopen that decision with evidence and the appropriate owner; continue unaffected integration.

Handover includes the current preview, design/resource map, actual approval source, connected task outcomes and observed conditions. The next developer can then distinguish a studied reference, adopted implementation and accepted product result.

## Preserve the foundation through real integration

Carry the accepted page/block relationships and behavior into the current product rather than rebuilding their surface from memory. Keep source configuration and adaptation controls identifiable. Replace fixture boundaries with the real application's owners, preserving hierarchy, content measure, state continuity and editable design decisions. Reassess only the affected foundation choice when actual constraints materially change its fit.

## Carry asset sources and delivery through Finish

Resolve each significant asset to its authorized master, reproducible export and actual delivery variants. Map theme, crop, density, locale or runtime state to the correct file. Retain source/notice requirements and publish only material permitted for the destination. Keep protected masters within their authorized locations.

Verify actual URLs, MIME, loading/cache behavior, decoding and dependency support in the product host. Recheck real text and state transitions after replacing fixtures; compare the exported spatial/material result in the target runtime. Validate delayed/failed loading, quiet/static alternatives and cumulative rendering cost. Deliver the editable source, transformation settings, usage locations and observed limits appropriate to the scope.

## Connect content to real product truth

Before replacing fixture values, map important strings to their actual source: brand vocabulary, product copy, service responses, localization catalog, business rule, price, eligibility, permission or persisted content. The trusted owner supplies protected facts and action outcomes. The application selects the right text for loading, success, failure, recovery and conditional display; design components render it in the accepted hierarchy.

Carry consistent user-level labels through routes, notifications and documentation. Keep translation keys and dynamic substitutions meaningful, encode values safely, preserve formatting and verify supported locale variants. Test that interface promises match actual results: saved, submitted, paid, published and delivered are distinct states. Material new contractual or product claims receive the appropriate approval. Preserve the reviewed text composition under genuine content lengths, themes and accessibility requirements.

## Prepare data with correct authority and lifetime

Map preparation to the real operation before moving it earlier. Distinguish read-only calculation from creating an offer, consuming a quota, reserving stock or submitting an order. The trusted owner decides protected values and validity. A prepared quote can accelerate display while checkout still follows its validation or reservation contract; client readiness and animation completion do not extend its validity or prove purchase success.

Identify the inputs that make a cached or in-flight result reusable: object and variant, user/permission context, quantity, currency, rule revision and any relevant time window. Invalidate or revalidate when those inputs change, and handle expiration while the page remains open or resumes from the background. Keep personalized results within their authorized scope. Match HTTP caching to the server's freshness and privacy policy; application caches also need their own keys, ownership and lifetime. [HTTP caching guidance](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) explains freshness, revalidation and response variation.

Bound concurrency, deduplicate matching work and preserve per-object progress and recovery. Give direct user actions priority over optional preparation. Reconcile out-of-order responses against current intent and the result's validity. Abort supported obsolete reads and release resources, using mechanisms such as [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController); reconcile consequential operations with their trusted owner because a locally aborted wait does not establish server rollback. A lost response can leave an outcome unknown, requiring status recovery before a retry could duplicate it.

Measure the complete task with the actual adapter as well as the reproducible fixture. Verify cold entry, warm reuse, rapid independent actions, expiration, input changes and partial failure at the affected boundary. Preserve correctness and input responsiveness while checking the resource cost of preparation. Record the observed improvement and remaining service dependency.

## Support content maintenance and operational work

Trace maintained content from its editing source through validation, localization, rendering and publication. Establish who can change it, which surfaces consume it and how the current value is determined. Where the product needs templates and individual overrides, define inheritance and reset behavior, distinguish missing values from intentional emptiness, and preview which objects a shared change affects. Use the existing content model when it expresses these responsibilities clearly.

Test replacement images, long names, optional fields, special values, rich text or Markdown, translation changes and new records in the actual components. Render authored content through the project's safe content boundary. Preserve the design's hierarchy as data changes; important business conditions remain visible at their decision points. Keep editable sources, locale versions and asset references maintainable at their actual owner.

Design batch operations from operator frequency, scale and exceptions. Make selection scope explicit across filters and pagination; show what will change and preserve individual control where needed. Enforce permission and validation per affected object. Report completed, failed, skipped, pending or unknown results according to actual outcomes, retain successful work, and offer retry or correction for the appropriate remaining scope. Distinguish a stopped client wait from cancellation of queued or completed work. Use atomic application, partial completion or rollback according to the underlying contract and expose the resulting behavior clearly.

Present the same underlying service state according to each role's task and access. A customer needs the impact on availability, commitment and next action; an operator may need the reason, affected objects and a diagnostic or recovery route. Derive both from the same business truth, retaining authorized detail at the appropriate surface. Verify cross-role consistency, persistent results, override behavior and recovery through actual UI paths. These operational choices apply where the product has maintained content or repeated management work; a static artifact uses its simpler publishing and editing boundary.
