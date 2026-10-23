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
