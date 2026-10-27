# Assurance and evidence

## Release assurance model

This release is assessed through source review, logical scenario analysis and
deterministic engineering checks. These establish different facts:

| Evidence | What it supports |
|---|---|
| File-by-file review | Responsibilities, writing quality, causal clarity and useful execution guidance |
| Logical scenarios | Whether the documented rules lead to coherent behavior in representative situations |
| Unit and failure-path tests | The exact optional-helper and release-tool behaviors exercised |
| Package/link checks | Portable structure, version agreement and resolvable local references |
| Repeated builds and inventory hashes | Reproducible distribution bytes and identifiable source content |
| Standard Skills CLI smoke checks | Discovery/installation, installed file identity and helper execution |
| Actual product browser review | Visual quality and task behavior in the observed UI scope |
| Real integration tests | The authority, persistence and outcomes exercised in that environment |

The final two rows require an executed interface and its actual boundary. The
repository fixtures provide scoped observations; consuming products establish
their own outcomes. Host-model understanding and comparative design quality need
their own observations. Large comparative agent campaigns are optional research,
rather than a release prerequisite.

## Run deterministic checks

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
python tools/package.py
```

The source includes tests for preparation safety, preserving existing files,
coverage requirements, stale/missing evidence, scoped approval and real connection
records, local path boundaries, installed helpers, version handling, content
inventories, reproducible archives and release readback/failure behavior.

The original 1.0.0 bundle's 47 tests were rerun successfully before changes. The
current test count and output are provided by the test command and each CI run.
A fixture named as test evidence is synthetic; its purpose is record validation.

## CI and installation

The workflow runs Python 3.10/3.13 on Linux and Python 3.13 on Windows/macOS. Its
installation job uses Node 24 and Skills CLI 1.7.4 in disposable projects. It tests
the local checkout and, on main pushes, the exact committed GitHub source, for
Codex, Claude Code and OpenCode installer targets. Installed bytes are compared
with the source; copied helper scripts execute from the new project directory.

This checks the installer, not a model session in each host. Read the Actions run
for executed jobs, logs, failures and any skips. Merely including a workflow is
not evidence that its jobs passed. The release job requires test, install,
publication and scenario checks, then verifies downloaded asset bytes before
publishing its draft release.

## Logical scenario review

The [file review](REVIEW.md) includes reasoning paths for users with open or precise
direction, continuation, subjective feedback, shared-shell changes, integration,
static products and unavailable verification capabilities. Scenarios are inspected
for contradictions, excessive process, lost requirements and role overreach.
Their expected behavior is distinct from a measured model outcome.

## Acceptance in a real project

Use the skill's verification reference: declare scope, inspect actual viewports,
complete tasks, review variants and transitions, repair causes and recheck affected
surfaces. At finish, verify both the accepted design and actual business outcomes.
Report approval, connection, verification and release separately.

Project evidence containing private data stays within its authorized location.
Publishing this skill does not publish a consuming project's screenshots or data.

## v1.2 publication and professional content

The professional expansion is reviewed as a connected model: content meaning,
concept, representation, concrete visual grammar, material/medium, timing,
observation and editable realization. Conditional patterns include both useful
applications and circumstances that call for another approach. This is source and
logical review, not a model-quality benchmark.

The publication job generates Chromium captures for the English and Chinese
READMEs at 390×844, 768×1024 and 1440×1000 in light and dark. It checks local
Markdown rendering, then the actual GitHub host on main pushes. Reports identify
the renderer and source commit. The job checks image loading/selection, native
installation text, disclosure behavior and document overflow; visual judgment is
performed separately by looking at the captures.

`tools/readme_art.py --check` verifies deterministic source artwork. Package tests
check its inclusion, inert SVG, image alternatives and source references. Optional
preview dependencies are isolated from the standard-library skill helpers. The
README design record states the observation conditions and evidence limits.

## Resource discovery assurance (1.3)

The local lookup and generated map have deterministic regression coverage for
schema, need/stack/form filters, exact item identity, empty results, provenance,
date preservation, installed execution and archive inclusion. The standard
installer smoke check also runs the installed lookup from its new project.

Release work rechecks selected primary access mechanisms and exercises catalog
queries. Those observations validate retrieval paths and source interpretation,
not every candidate's runtime or visual quality. [The resource review](REVIEW-v1.3.0.md)
connects accepted requirements to code and documentation. The actual CI result
identifies executed jobs; source presence alone does not establish a passing run.

## Product-intent scenario

`python tools/validate_scenario.py --output-dir scenario-evidence` executes the
included research-model comparison with real browser input, dialogs, theme
changes, failure/retry, cancellation, long content, reduced motion and local note
persistence. Four viewports × two models × two themes produce 16 primary captures;
additional active/error/edit/scroll captures document important states. Targeted
color pairs and a synthetic input-to-frame sample are measured.

The optional `--in-memory` mode renders exact local source without navigation.
It exercises the storage-unavailable path and marks persistence pending. CI uses
HTTP, and its successful job is required for release. Actual images are opened
for visual judgment separately. The [scenario record](../examples/product-intent/README.md)
contains sources, reuse decisions and explicit boundaries. Owner acceptance of a
real project and independent model behavior remain separate evidence.

## Foundation evidence

The source mapping identifies an actual page-level foundation and the major
relationships preserved by its native port. The scenario checks realized width,
composer radius, empty-state type and actual task continuity alongside its viewport
captures. A public upstream preview can be captured with `--source-preview`; the
runner verifies the pinned source blob and records live access separately.
This remains a scoped example, not an upstream-runtime or model-quality certification.

## Visual asset assurance (1.5)

`python tools/validate_assets.py --output-dir scenario-evidence/assets` runs an
HTTP browser fixture against existing README illustrations and a sourced Lucide
icon. It checks actual file identity, responsive/theme selection, small CSS sizes
at two densities, informative/decorative/functional semantics, blocked-resource
fallback, preserved layout, motion pause/reduced preference and inactivity policy.
Captures and measurements state their environment. The scenario job runs this
with the existing product fixture before release.

The publication illustrations retain their editable Python source and four SVG
outputs. The fixture ships the selected icon and required notices, while fonts use
the environment's installed system stack. Specialist 3D, custom font and authored
animation-tool pipelines are method/research coverage rather than executed claims.

The asset runner's optional `--in-memory` mode supports hosts that cannot navigate
a local server. It embeds actual local source bytes and exercises an invalid-image
decoder result; it explicitly leaves HTTP delivery unverified. The CI command uses
the default HTTP path and is a required release check.

## Content design assurance (1.6)

The content example validates wording/state mapping, visible and accessible names,
two locales, two themes, representative viewports and real browser-local storage.
Read, write and removal faults exercise truthful recovery at the native Storage
boundary. Controlled-clock cases cover edits during a save, repeated submission,
clearing pending work and language changes; they establish state ordering rather
than a performance score. The report lists each viewport/full-document capture
and records native persistence separately from the optional simulated mode.

Automated checks establish declared DOM and action observations. Opened screenshots
support actual visual judgment; independent user comprehension requires its own
observation. The content source map documents adopted methods rather than claiming
that referenced design systems certify this skill.

The [1.6 review](REVIEW-v1.6.0.md) records the executed local checks, observed repairs
and one fresh-context forward application to an image-organizing tool. That task
produced a design proposal, researched sources and proposed verification; it did
not implement the tool or measure a performance improvement. The nine experience
dimensions guide judgment while each claim retains its own evidence boundary.

## Visual reasoning and temporal assurance (1.7)

The [visual observation guide](VISUAL-INSPECTION.md) describes the common method;
the [temporal fixture](../examples/temporal-review/README.md) provides a bounded
runtime in which to exercise it. The browser runner generates chronological
visual evidence and checks declared action/state relationships. Its report
identifies source content, viewing conditions, trigger and capture timing, and
the time-control mode where one is used.

Captured media and actual visual inspection are separate records. Opened frames
support judgments about those moments and their observed relationship; normal-time
playback supports the pace of the recorded interval under its capture conditions.
Controlled-time probes help isolate ordering and intermediate geometry. Sparse
samples or encoding frame rates cannot establish application frame delivery or
rule out a stall between samples. Motion/performance claims require matching
observation and runtime evidence.

Assess source-resource appearance, the assembled composition and the delivered
runtime at their respective boundaries. Link consequential findings to a visible
relationship, its likely perceptual effect, a cause to investigate and the result
of the correction. Actual user comprehension, owner acceptance and comparative
agent performance remain independently established outcomes.

The version review records the checks actually executed, the media actually viewed,
observed repairs and remaining conditions. CI retains its actual assertions and
capture artifacts. A consuming product follows the same method using its own
content, services, devices and user journey.

## Product alignment and active exploration assurance (1.8)

The [alignment guide](PRODUCT-ALIGNMENT.md) connects target experience, research
questions, actual observation, resource adaptation and verification in use.
Review the common instructions for that connected behavior, including open briefs,
named product analogies, reference-object attribution and decision-based convergence.
Text or keyword presence alone does not establish that an agent performed research.

For a forward application, provide a frozen skill and an ordinary task in a fresh
context. Retain the input identities and requested scope. Let the agent choose
its sources and actions; keep the maintainer's diagnosis, expected choices and
other applications outside that context. Inspect the produced artifact and actual
tool evidence after the task. A scheme-only brief establishes research and design
decisions; a runnable brief can additionally establish the implementation and
specific runtime conditions exercised.

Judge useful evidence coverage: what experience was selected, what was actually
seen or operated, how findings changed the choice, which resource carries the
relationship, and whether the current result answered the original question.
Record blocked access and partial temporal observation without expanding the
conclusion. Keep these applications distinct from the deterministic fixtures,
installation checks, real-user outcomes and a comparative model campaign.

The [version review](REVIEW-v1.8.0.md) records the actual applications, checks,
viewed conditions and limits. Existing product, asset, content and temporal gates
continue to exercise their declared runtime contracts before release.

## Mature implementation and local-trial assurance (1.9)

The [resource reuse guide](RESOURCE-REUSE.md) connects a craft target to actual
implementation adoption. Evaluate this through the produced source and observed
application: identify which mature structures, components, assets or behaviors
carry consequential UI responsibilities, why they fit and which mechanisms survive
adaptation. A studied reference establishes design evidence; an installed package
establishes availability. Each implementation and quality claim needs its own
support. Dependency counts, code ratios and matching instruction keywords do not
establish retained design value.

For an ordinary fresh-context application, inspect the agent's actual sequence:
which reference qualities guided the resource comparison, which consequential
candidates were trialed under current content and states, and what the trial
changed before wider integration. Keep reference, upstream demonstration, local
trial and assembled journey observations distinct. A verified system can cover
routine instances under matching conditions. Let the user task determine useful
coverage rather than prescribing a library, source count or expected result.

Review adaptation through concrete source changes and rendered behavior. Public
configuration and composition may preserve mature relationships; changed layout,
state or motion mechanisms expand the current implementation's verification
responsibility. Check that custom work addresses an identified gap and that the
complete product is inspected after the parts are combined. Target changes,
remaining quality gaps and user-assisted acquisition keep their actual scope and
authority. A local fixture does not establish a live service outcome.

Use the [version review](REVIEW-v1.9.0.md) to record applications actually performed,
source identities, adopted implementations, local-trial and final evidence,
repairs and remaining conditions. Distinguish those observations from source
review, package/installer checks, authored regression fixtures and real-user
acceptance. The existing release gates retain their declared boundaries.

## Human-centered perceptual assurance (1.10)

The [visual guide](VISUAL-INSPECTION.md) and runtime principles provide a multiscale
method: inspect at intended scale, deepen into consequential regions and details,
then revisit the complete interface and continuous task. Judge whether observations
identify concrete relationships, distinguish visible facts from effects or causal
hypotheses, and change or justify resource selection, preservation and adaptation.
A dimension inventory or repeated method vocabulary does not establish execution.

In a fresh-context application, provide the frozen skill and an ordinary task with
raw source or visual material. Keep diagnoses, anticipated repairs, prior reviews
and sibling outputs outside the input. Inspect actual viewed evidence and the
resulting source, including local-to-whole rechecks. Preserve scale, crop, source
and time conditions. A professional reading of hierarchy or material remains
distinct from measured attention, user comprehension and preference.

Record executed applications and their limits in the [version review](REVIEW-v1.10.0.md).
Existing package, installation, publication and browser fixtures retain their
mechanical scope. Perceptual-method changes do not introduce a new numeric quality
gate, fixed capture count or additional installed dependency.

## Art direction and expressive experience assurance (1.11)

The [art-direction guide](ART-DIRECTION.md) connects familiar task relationships,
cross-domain expression, mature implementations and controlled production. Source
review checks whether explicit aesthetic goals retain their authority across
analysis, selection, system rules, adaptation and verification. Product categories
must remain task/operating context rather than automatic style restrictions.

Evaluate actual applications for decisions and outcomes: which expressive sources
were observed, which resources carry their relationships, whether meaningful
visual differences reach populated core work, and how concrete defects were
repaired. Review experience validity and expressive completion separately. A source
comparison additionally tests preservation of an identified design; its image
metrics do not establish artistic quality. Do not infer effectiveness from method
terminology, dependency counts or documentation length.

Use ordinary tasks and raw artifacts with frozen skill bytes in fresh contexts.
Keep expected styles, diagnoses and sibling outputs outside the inputs. A working
application can establish its exercised local behavior; an authored film establishes
its own source fidelity and viewed temporal output. Controlled frame capture,
normal-speed playback and measured runtime performance have distinct scopes.
Record sources, actual viewing, repairs and remaining conditions in the
[version review](REVIEW-v1.11.0.md). Existing deterministic and publication gates
continue without a new aesthetic score, mandatory style or installed dependency.

## Intent-grounded research and evidence maturity assurance (1.12)

The [experience research guide](EXPERIENCE-RESEARCH.md) connects user intent,
revisable experience hypotheses, question-led evidence planning and adaptive
exploration to actual adoption. Source review checks that current-user intent,
audience conventions and observed products retain their different authority;
text, renders and behavior retain their evidence limits; and meaningful new
findings can change both the product model and resource choice. Review additions
and deletions together so the richer research method preserves previous craft,
integration and proportionate-iteration requirements.

For a fresh-context application, freeze the complete skill and provide an ordinary
task with complete raw inputs. Keep the maintainer's diagnosis, expected resources
and anticipated solution outside the application. Inspect the actual source
visits, viewed media, revised questions, candidate differences, adoption decisions
and produced result. Record any input correction or later review-directed repair
separately. A scoped local edit should be able to reuse an accepted direction;
an open product brief should establish the experience and consequential evidence.

Judge research by what it changed or justified. Search counts and elapsed time
describe activity; they do not establish sufficient exploration or better design.
Hundred-step or hours-long research remains available for valuable uncertainty,
without turning that capability into a release test quota. Captured media, actual
viewing, source assertions, interpreted fit and owner acceptance keep their own
scope. A proposal can establish a feasible direction and scoped trial; it cannot
establish an unbuilt product's operational quality.

The [version review](REVIEW-v1.12.0.md) records executed checks, independent
applications, README self-application, source identities and limitations. Existing
product, asset, content and temporal fixtures remain deterministic release gates.
Their results do not measure general model improvement or human preference.
Publication readback is tied to the actual committed source and release assets.

## Multiscale design evidence: separate assurance tracks

Version 1.14 adds a structural helper and a reproducible preparation kit for
[three-arm behavior comparisons](experiments/design-evidence/PROTOCOL.md).
The baseline already contains evidence-oriented methods; the experiment tests
additional structure and action coupling, not the invention of research.
Frozen inputs and pending cells are preparation, not executed model runs.
No deterministic test, synthetic declaration or file hash establishes that an
agent searched, viewed, adopted or improved the interface. Record the actual
model/harness, tools, access, trace, implementation and blind visual review for
each run. Keep content integrity, observed behavior and perceptual outcomes
separate, including source-based hypotheses and untested dimensions.

## Structural boundary assurance (1.15)

Boundary regression tests exercise the ten requested cases: empty-but-readable
structure, theoretical missing categories, one candidate, high-impact gaps,
unviewed files, scoped engineering results without aesthetic inference, separate
waivers, reopened decisions, declared-relation candidates and bounded routine work.
They establish tool behavior, not independent Agent effectiveness or UI quality.
Read-only file safety and explicit digest comparison retain their own assertions.

The earlier three-arm inputs stay identified as their original prepared experiment.
Do not count them or synthetic record tests as new model runs. A maintainer's real
application can provide scoped workflow evidence; independent matched Agent runs,
actual tool traces and blinded UI review are separate empirical work. Report
unexecuted comparisons without substituting a pass from the structural inspector.


## Additional scoped source applications

The [v1.16.1 reconciliation review](REVIEW-v1.16.1.md) links three current-maintainer
application families: a conversation block, an expressive reading workspace and
an input-controlled drawer. Source identity, real operations and viewed frames
support their stated observations. They are not independent Agent samples,
complete product parity, a controlled model comparison or general aesthetic uplift.


## v1.14 post-release empirical acceptance — owner and blind Agent review

The original `v1.14.0` preregistration remains frozen as a before-run record. The later [18-run evidence report](experiments/design-evidence/RESULTS-v1.14.0.md) and [structured trace summary](evidence/v1.14.0/empirical-findings.json) preserve the separate anonymous Agent preferences and the 2026-10-28 human product-owner preference.

The owner explicitly accepts the **structure + action** direction for improved personal visual impression, perceived spatial smoothness and color harmony. The 12 locked Agent judgments are mixed (T02 favors structure + action, T01 does not) and remain unchanged. T06's eight recorded pixel conditions are identical between arms. Hence report **positive owner acceptance in this sample**, rather than either “empirical work unexecuted” or “universal objective visual superiority.” The tagged production skill contains both map and action rules; the ablation arm is not an identical production artifact.
