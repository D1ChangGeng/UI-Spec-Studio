# T1 mobile theme route: independent method check

Scope: read-only inspection of `adapt_theme_route.py`, its recorded `PLAN.json`,
the three original/adapted instrument diffs, original n7c9d9ca8 group 09 failures,
and that output's frozen `App.jsx`. Adapted observations were in progress; this
review makes no statement about their eventual pass/fail result or visual quality.

## Assessment

The proposed adaptation is a justified access-route correction within the
protocol's allowance for demonstrably equivalent public behavior. It does not
repair the application or change the registered success criteria.

- The original primary and supplemental group 09 failures are locator timeouts
  waiting for `theme-toggle` at the narrow condition. Earlier inspected theme
  assertions exist in the preserved raw records; the adaptation does not erase
  those failures.
- The frozen application already renders its theme button inside `sidebar`.
  Above 720px the sidebar is present directly; at narrow widths it appears through
  the existing Radix history dialog opened by `history-toggle`. The existing
  theme handler updates React theme state and its root appearance effect.
  The inspected `App.jsx` still matches its frozen SHA-256.
- The added helper conditionally clicks visible `history-toggle`, clicks the same
  existing `theme-toggle`, then closes the opened history dialog with Escape and
  waits for its theme control to become hidden. It uses ordinary public UI
  actions: no forced click, hidden-element evaluation, injected application
  state or test-specific application patch.
- The same helper and three adapted scripts are scheduled for all four assigned
  T1 outputs: nb8be8a13, n08f925c8, nc5f68f67, n7c9d9ca8. The condition activates
  according to visibility, not the output ID or version. Directly visible theme
  controls keep their original click route.
- The original evaluate, contract-supplement and settled scripts still match
  their registration and plan hashes. Their adapted copies match the plan's
  separate hashes. Inspection of the full diffs shows helper insertion and
  replacement of theme-click call sites only; assertions, thresholds, viewport
  sets, content and fixture behavior remain unchanged. `settled.mjs` also has
  an equivalent replacement in its unused T2 branch, but this adaptation command
  invokes it exclusively with T1 and does not reclassify T2 observations.
- Outputs are written only under each run's new `routing-adapted` directory.
  Existing adaptation directories are refused. The script has no writes to
  participant code, raw primary/supplement results or registered instruments;
  it rechecks every frozen file after the adapted observations.

## Conditions for interpreting the eventual results

Use adapted group 09 only after the same route-aware observations are available
for all four T1 outputs, retain the raw and adapted group outcomes side by side,
and leave every other group's original outcomes authoritative as stated in the
plan. Use the uniformly adapted stable captures for the T1 visual packets.
An adapted execution completing does not by itself imply a passing assertion.
This review establishes the scope of the method correction, not an outcome.
