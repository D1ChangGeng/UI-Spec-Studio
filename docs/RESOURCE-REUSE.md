# Discover, assess and reuse excellent UI work

Resource discovery is part of design, not a separate user-managed research phase.
The agent looks for worthwhile existing work, understands why it is effective,
chooses a reuse level and verifies the result in the current product.

## The working relationship

**Goal → discovery → professional assessment → adaptation/composition → real verification → useful project knowledge.**

Requirement-led search finds an implementation for a known need. Opportunity-led
exploration finds a better expression while meaningful design choices remain
open. Both use the project's task, accepted direction and actual constraints.
Existing suitable choices carry forward.

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

## Select the useful level

Directly adopt an appropriate implementation; adapt its public configuration or
source; compose complementary behavior and visual capabilities; transfer an
understood technique; or implement a simpler native solution. Compare clarity,
visual value, required behavior, compatibility, rights and total cost from research
through maintenance. The result should belong to one coherent product.

Before integration, identify the exact variant/version, demonstration settings,
source/dependencies and changes to project files. Resolve the most important
unknown with a small representative probe. Inspect the complete result under real
content, views and states. Preserve the mechanism that earned adoption and the
behavior that makes the task reliable.

## Read platform mechanisms by responsibility

Indexes and galleries show possibilities. AI text and APIs explain contracts.
Copy/export may preserve the chosen demo settings. Registries and inspection CLIs
expose files, dependencies and supported changes. MCP may provide queries or real
writes; its availability and permissions come from the host. Project stories
supply incumbent components and states. Use the shortest reliable available route.

The [common reference](../skills/ui-spec/references/component-sourcing.md) explains
these mechanisms and their boundaries. Follow documented links and observe actual
results; missing access can be handled through another legitimate source.

## Keep useful records lightweight

For an important adoption, preserve the purpose, source/item/variant/version,
selected mechanism, reuse level, adaptation boundary, rights, project checks and
update owner. Existing component/design records are preferred. The optional
[adoption note](../skills/ui-spec/assets/templates/resource-adoption.md) is available
when a project needs a starting structure.

Platform documentation, item inspection and project acceptance remain separate.
Successful project-specific choices stay in that project. Portable findings can
enter the shared catalog through authorized maintenance and ordinary version
control. Add a new candidate when its source is credible and it supplies meaningful
coverage or a better fit; refresh relevant records when conditions change.

## Worked decision paths

| Situation | Useful path | Completion evidence |
|---|---|---|
| Existing approved menu still fits | Reuse it; inspect only changed conditions | Affected controls and actual states |
| New Vue account entry | Find a behavior primitive and coherent visual layer; read exact contracts | Keyboard, touch, dismissal, theme and real session results |
| Open visual direction | Inspect a small set of promising mechanisms; recommend and prototype | Whole-frame effect, readability, controls and combined cost |
| Font discovery | Use family catalog for glyphs; AI docs for usage | Real text, variants, loading and licensing |
| Cross-stack reference | Select native realization or transfer its technique | Current stack behavior and intended visual quality |
| Paid or unavailable resource | Resolve access/rights or use a viable alternative | Accurate remaining conditions and independent progress |
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
