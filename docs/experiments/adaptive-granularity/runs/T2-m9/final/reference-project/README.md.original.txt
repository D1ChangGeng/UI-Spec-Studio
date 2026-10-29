# Product intent study

A runnable, authored scenario for UI Spec Studio's **product model → references →
resource choice → visible result → review** workflow. Open [index.html](index.html)
through a local static server, or run the browser check below.

```bash
python -m http.server 8080 --directory examples/product-intent
python tools/validate_scenario.py --output-dir scenario-evidence
```

The sample uses fictional research content. Research replies are simulated;
notes use one local browser record. This is a reusable workflow demonstration,
not the user's application, an approved redesign or an independent model trial.
The original screenshot and private source are kept outside this public example.

## Evidence and intended use

The motivating report described a research product whose generated appearance
and resource use did not communicate a sufficiently grounded direction. The
supplied still frame showed a composer, research history and a recent-work region.
A still frame supplies layout evidence; it does not establish the generating
agent's tool use, the full product behavior or runtime performance.

For this bounded example, the assumed task is to start a research question,
inspect an illustrative result with its source, continue the thread, and revisit
work. A second hypothesis prioritizes durable notes. The actual product owner
would confirm which is primary from real use and intent.

## Consequential choice

| Direction | First action / enduring object | Continuation | Fit and tradeoff |
|---|---|---|---|
| **Conversation — recommended for this assumed task** | Ask a question / thread | Read, inspect a source, ask a follow-up | Direct start and continuity; documents remain supporting objects |
| **Information space** | Open/create a note / document | Edit, organize and return to the collection | Strong durable organization; asking a question becomes a secondary action |

Both use the same content, color roles and source materials so the comparison
isolates the interaction model. The selector changes the actual primary action
and working region. Its visible status remains **pending owner confirmation**.
Changing the selector records a local preview preference, not project approval.
A task-centric model was considered from Linear's documented issue/project model;
this sample's assumption lacks assignment/status management as the primary loop.

### Product-pattern sources

Sources inspected on **2026-10-25**. These document specific conventions rather
than the complete current products or their performance.

- [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt): related chats, files and instructions support continuing work.
- [Claude Projects / Artifacts](https://www.anthropic.com/news/projects): the June 2024 product article describes conversation with a dedicated adjacent artifact; this historical example supports the relationship, not a claim about the entire current UI.
- [Notion databases](https://www.notion.com/help/intro-to-databases): durable pages with properties and multiple collection views support object-centered work.
- [Linear projects](https://linear.app/docs/projects): outcome-bound groupings of issues support a different task/operational model.

## Design and resource selection record

Rows were selected before the representative implementation and reconciled with
the actual source. Documentation/source inspection, implemented behavior, browser
checks and owner approval remain distinct. Browser results are in the generated
report and CI artifact; owner acceptance of a real project stays pending.

| ID / surface / dimension | Product convention and intended effect | Exact implementation source / reuse level | Reason and adaptation | Actual implementation and check |
|---|---|---|---|---|
| D1 / study navigation (supporting probe) | Project/thread continuity; collection navigation changes with model | [shadcn Sidebar anatomy](https://ui.shadcn.com/docs/components/radix/sidebar), structural technique transfer | Stable header, scroll owner and usable narrow navigation; authored HTML rather than installing a React runtime into this static fixture | `.sidebar`, `#history-dialog`; narrow dialog, focus return and shell overflow |
| D2 / conversation input | Question starts the primary loop; input remains available during results | [shadcn Input Group](https://ui.shadcn.com/docs/components/radix/input-group), structural technique transfer | Group text and actions; preserve native form semantics and controls | `#composer`, `submit()`; send, stop, retry, draft and stale-result checks |
| D3 / surfaces and background | Long reading and clear grouping | [Radix Colors scale roles](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale), actual Slate values adapted | Slate study chrome supports the adopted assistant page's monochrome reading roles; actual paired contrasts are measured | `tokens.css`; light/dark primary, secondary and action contrast pairs |
| D4 / resource source identity | Same as D3 | [Pinned source](https://github.com/radix-ui/colors/tree/dbdb85470547c7d34b9001f48fddb08ded335979), sRGB Slate and Slate Dark | Values retained, variable mappings authored locally; MIT notice preserved | `THIRD-PARTY.md`, `tokens.css`; source-value regression |
| D5 / overlays | Inspect evidence then return to the same task | [HTML dialog](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog), native implementation | Fits the dependency-free sample, with focus return and Escape; a Vue product can instead assess [Reka Dialog](https://reka-ui.com/docs/components/dialog) | `#decision-dialog`, `#source-dialog`; actual open/dismiss/focus checks |
| D6 / typography | Read content and distinguish controls from supporting context | System font stack, original arrangement | CJK fallback, finite roles, no remote font payload | `styles.css`; actual Chinese render at four widths |
| D7 / icons and assets | Identify frequent actions clearly | Text labels and native symbols, authored | Text carries meaning; a small local sample needs no decorative icon runtime | Buttons and labels; accessible names and keyboard operation |
| D8 / micro-interactions | Feedback belongs to the current user intent | Native form events/timers, authored | Draft preservation, cancellation and token ownership isolate state | `app.js`; slow/failed/repeated/model-change checks |
| D9 / general and text animation | Repeated reading and input remain stable | Local state/background transitions, authored | Short control feedback; text stays stationary; reduced-motion equivalent | `styles.css`; reduced-motion computed style and runtime tasks |
| D10 / document state | Durable page in a collection | Notion convention; browser local storage, authored fixture | One sample note can be edited, saved and reopened; no service claim | `openNote()` / `save-note`; HTTP-browser edit/save/reload |
| D11 / assembled experience | Coherent model rather than independent widgets | All selected sources in the page | First use foregrounds the composer; supporting evidence joins active work | Whole-view capture, long-thread scrolling, theme/draft retention |

External behavior/resource descriptions came from the linked primary material.
Product reference layouts and branding are not copied. Actual reused color values
are attributed; remaining source is original implementation or identified
technique transfer. The 37-resource catalog remains a search space rather than a
requirement to add effects to a reading-focused interface.

## Verification boundary

The browser runner exercises both directions and themes at 390×844, 768×1024,
1280×720 and 1920×1080. It captures whole viewports, opens the decision/source
panels, checks targeted color pairs, performs submit/stop/retry, prevents stale
completion after model changes, tests local note persistence and checks long
content plus reduced motion. It records one input-event-to-next-frame observation;
this is a local synthetic observation, not field INP or service latency.

`--in-memory` renders exact source offline where local navigation is unavailable.
That mode verifies the explicit storage-unavailable path and leaves persistence
pending. The CI HTTP run exercises real browser local storage and must pass before
release. Open the output images to make the visual judgment; DOM checks alone
establish only their measured conditions. Actual model effectiveness and original
product integration require their respective evidence.

## Page-level foundation

The conversational direction now starts from a concrete mature page rather than
independently authored major regions. [The foundation record](FOUNDATION.md)
explains the candidates compared, chosen granularity, inherited relationships,
precise source identity and deliberate adaptations. The source map is in
[foundation.json](foundation.json). The document direction remains a comparison
probe; real product intent and acceptance remain open.

This is a whole-page design transfer into the native fixture. Runtime integration
is a separate adoption decision for the consuming product's actual stack. The
browser checks inspect the realized relationships and state paths rather than
using attribution alone as evidence of quality.
