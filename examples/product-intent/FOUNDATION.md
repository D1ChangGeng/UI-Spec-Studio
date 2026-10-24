# Conversational page foundation

The selected starting point is the [assistant-ui ChatGPT page example](https://www.assistant-ui.com/examples/chatgpt),
with [source pinned to 1fbf00dd](https://github.com/assistant-ui/assistant-ui/blob/1fbf00dd0388fee912af95401876a6cc3c232b2c/apps/docs/components/pages/examples/chatgpt.tsx).
The reviewed source blob is `0f22e7855a954269ecdee0fd9963240c966e1bc1`.

## Why this reuse level

The assumed task starts with a question and continues through a thread. The
complete page already coordinates the welcome composition, primary input,
reading measure, user/assistant distinction, action placement and active-state
layout. Inheriting those relationships together resolves more consequential
choices than selecting a color palette and an isolated input.

The official shadcn dashboard-01 was compared as a page-level alternative. Its
metrics/chart/table hierarchy serves an operational overview rather than this
primary loop. Sidebar-07 is a useful shell-level candidate but leaves most of the
conversation composition unresolved. These are task-fit decisions, not universal
quality rankings.

## Inherited relationships and actual locations

| Source relationship | Project realization | Observation |
|---|---|---|
| Empty heading and composer grouped above center | `#conversation`, `.welcome`, `#composer` | Whole empty-state viewport at four sizes |
| Shared 48rem reading/composer measure | `--chat-width`, `#conversation` | Computed width and active-state render |
| 24px/28px regular empty heading | `.welcome h1` | Actual Chinese rendering; narrow adaptation recorded |
| 28px composer; state-prioritized send/cancel | `#composer`, `#send`, `#stop` | Source radius, input/cancel/retry tasks |
| 70% bounded, right-aligned user message with 22px radius | `.message.user` | Active-state geometry; 85% phone adaptation |
| A stable reachable composer during growing results | `.has-result #thread`, `#composer` | Long-content scroll and input retention |
| Coherent light/dark reading and composer roles | Root tokens in `styles.css` | Targeted actual contrast pairs and rendered themes |

The adoption method is **page-level design transfer into a native fixture**.
It inherits the page's coordinated design decisions; it does not install the
upstream React runtime. For a compatible real React product, adopting the actual
components/runtime is a candidate before rewriting their behavior. This fixture's
portability constraint is local, not a default implementation policy.

Research copy, source inspection, local note behavior and accessible phone targets
are explicit product/fixture adaptations. Voice, attachments, hosted history and
real research services are outside this sample. Document-first remains a bounded
comparison probe. The actual product owner still selects the product direction.

The official documentation and exact source were inspected on 2026-10-25. The
native projection is rendered and exercised by the scenario runner. Upstream live
browser observations, when available in the release evidence, retain their actual
URL/date and are separate from the pinned code and the adapted sample.

See [the decision record](README.md), [machine-readable source mapping](foundation.json)
and [preserved notices](THIRD-PARTY.md).
