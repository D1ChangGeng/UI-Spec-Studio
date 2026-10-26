# UI Spec Studio 1.10.0 review

## Scope and accepted behavior

This release implements Human-centered Visual Inspection & Perceptual Design
Analysis within the existing product-alignment, active-exploration, temporal and
mature-adoption method. It develops the user's whole-to-detail observation model
into runtime guidance, connected resource decisions and inspectable application.

| Accepted requirement | Responsible implementation |
|---|---|
| See, understand and apply real design | SKILL establishes the default; analysis connects product questions to perceptual interpretation and actual selection |
| Whole impression, composition, region, detail and return | Principles owns the multiscale method; workflow, verification and integration arrange contextual reinspection |
| Nine flexible perceptual dimensions | Principles provides selective lenses for attention, space, type, color, material, shape, assets, movement and system identity |
| Explain craft and optical relationships | Principles connects intent, precision, coherence, suitable expression and stability in use; assets distinguishes visible drawing size from control targets |
| Extend analysis through time and the product | Interaction and verification preserve meaningful episodes, normal-speed/detail/normal-speed observation and related-view continuity |
| Turn observation into adopted mature work | Sourcing compares intrinsic quality, product fit, retained relationships and integrated quality through original demos and current-content trials |
| Make decisions executable and verifiable | Optional templates connect visible fact, likely effect, relationship or hypothesis, product fit, actual implementation and inspected result |
| Converge through decision value | Existing operations retain impact-based depth, shared verified rules and explicit evidence gaps |

The detailed runtime method belongs to `principles.md`; the other references call
it within their existing responsibilities. The public [visual guide](VISUAL-INSPECTION.md)
explains the same method with conditional examples. The nine perceptual lenses
and the nine product-experience dimensions have distinct roles: one investigates
visible relationships, the other locates design responsibilities.

No new stage, compulsory record format, aesthetic score, capture quota, runtime
dependency or host power is introduced. Mature implementations remain the default
for common UI, with bounded customization for evidenced gaps. Design inheritance,
actual adoption and verified current-product quality remain separate facts.

## Source consistency and context budget

The maintainer read the entry, eight common references and integration in full.
A separate read-only pass reviewed those current files and their diffs against
v1.9.0, then checked the public guide. It found no blocking contradiction or lost
responsibility. Removed section headings have no remaining in-repository Markdown
anchor references. Existing temporal evidence, normal access, local-trial,
controlled-adaptation and real-user evidence boundaries remain explicit.

The common references total **145,332 bytes**, compared with 143,387 in v1.9.0,
under the unchanged 147,456-byte test limit. SKILL is 142 lines with a 963-character
description. These measurements describe packaging and reading cost; they do not
establish model comprehension or visual quality.

## Independent application setup

Two fresh-context tasks received an ordinary improvement request, a read-only
copy of the skill and raw project source. They received no maintainer diagnosis,
anticipated repair, previous review or sibling result. The first received 27
source/lock/test files from the prior local question workspace; the second received
14 source/lock/test/notice files from the prior local reading tool. Prior reports,
research captures and diagnostic scripts were excluded.

Ten method files were frozen before either application: SKILL, the eight common
references and integration. The SHA-256 of their path-sorted compact JSON hash map
is `311681aca058b51b277b7644117e98a21eb38ba4acb2ede1202444c059ba0814`.
Available Chromium, Python browser dependencies and CJK-font paths were supplied
as neutral execution context. Copies of existing dependencies were later offered
as an optional cache, without prior application evidence or design advice.

The applications operate on synthetic local products. They are bounded observations
of these tasks, not a controlled model comparison, actual audience research or
certification of all visual media. Their source identities, adopted resources,
actual observations and remaining conditions are recorded with the results below.

### Question workspace

The ordinary task was to improve the existing local material/question workspace
for long Chinese and English content on desktop and phone. The author first
inspected the whole product, then material rows, writing controls, text and
related states. The existing left-material/right-reading structure, quiet green
identity and explicit preset-answer boundary remained appropriate.

Actual implementation retains Mantine 9.7.4: AppShell owns the fixed shell and
breakpoint offsets; Textarea owns native editing and autosize; Modal, Drawer,
Menu, Checkbox, Button and Dropzone keep their existing interaction mechanisms.
Tabler 3.49.0 remains the icon family. The author operated the original AppShell
and Textarea demos through the provided browser, then inspected the existing
local trial and current-content application. Modal documentation was read; it is
not described as operation of every upstream Modal demo. External demo images
were viewed in the browser response, without a separate project image archive.

Adaptation concentrates on the observed relationships: a 304px material region,
clearer selected rows and file metadata, coordinated text/surface weight, a visible
expansion action, bounded long-question previews, and distinct Chinese/English
reading treatment. The model, storage, importer, package declaration and lock
remain byte-identical to the input. No new dependency or replacement autosize
engine was introduced.

Three actual findings illustrate how perceptual inspection and engineering
evidence affect each other:

| Observed condition | Investigation and decision | Rechecked result |
|---|---|---|
| At 390×844, example entry hid the question metadata behind the fixed header | Baseline geometry and source showed that `scrollIntoView` also moved the outer page. Scroll only the reader; focus with `preventScroll`. | Outer scroll changed from 64px to 0; reader starts at 64px. The same Chinese example now shows metadata and the complete question below the header. |
| At 844×390, a 1,332-character draft looked empty although its counter and submit action remained | The initial autosize/height hypothesis was revised: two trailing newlines occupied the roughly two-line viewport while the browser correctly retained the end caret. Increase the short-height cap from 72px to 96px. | The same unchanged draft shows its trailing sentence. Reading space remains 121px in landscape and 174px at 390×440; writing actions remain visible. |
| Short-height styling hid the 50-turn capacity explanation | Keep the capacity message while compacting ordinary shortcut help. | A test creates 50 turns through the UI, checks the message and continues through new-topic recovery. |

The blank draft was a visible-context problem, not evidence of data loss. The
diagnostic record preserves the original hypothesis, cursor comparison, unchanged
text and revised explanation. A separate reviewer independently found the blank
presentation, then reopened the repaired frames; the maintainer also viewed the
preserved original and final pixels. The additional input space is recorded with
its reduced reader-height tradeoff. The 390×440 condition is a reduced-height
proxy, not an actual handset keyboard.

![Same Chinese example after reader-owned scrolling; metadata stays below the fixed header](evidence/v1.10.0/question-after-mobile.png)

The retained [baseline](evidence/v1.10.0/question-before-mobile.png) uses the same
viewport and example. The [desktop result](evidence/v1.10.0/question-after-desktop.png)
shows the integrated material and writing regions.

![Intermediate landscape draft with no visible body text despite a nonzero count](evidence/v1.10.0/question-landscape-before.png)

![Same draft and trailing newlines after the short-height refinement](evidence/v1.10.0/question-landscape-after.png)

After the last source change, the full **9-scenario browser run passed**, with
zero skips or flaky results, in 54.8 seconds. It covers imports, edits, selection,
questions, clipboard/export, reload, removal/undo, errors/recovery, IME guards,
English, reflow, keyboard/focus, capacity and long-draft rotation. The production
build passed. Four Axe states reported zero violations; one unresolved automatic
background judgment remains in the raw record and has a scoped follow-up showing
uncovered `#657164` text on white at 5.12:1. This is not full accessibility
certification. Recorded local feature paths had no external requests, non-GET
requests or runtime errors.

The separate visual reviewer opened all **23 final frames**, six relevant baseline
frames and the retained defect image, plus seven detail crops. Six changed final
frames were reopened; the other 17 remained byte-identical. No visual blocker
remained. The review retains minor observations about truncated filename previews
and a partially clipped first line at an internal text-scroll boundary, without
inferring an interaction failure. Ordered episode frames have capture-time brackets
and keep their viewing scope separate from motion claims. Ten episode files were
captured; during iteration the author actually judged the complete images named
`02`, `03`, `05` and `06`. The `04` tool return was not sufficient for a complete
frame judgment, and the other five episode files were not individually opened by
that author. Similar final-state screenshots do not replace those missing episode
observations. These path-based iteration observations have no frozen-at-view hash
record, so they are not presented as a final-version full-episode review. No
normal-speed continuous playback was performed.

The build retains its main-chunk-over-500kB warning. Real handset keyboards,
Safari/Firefox, human screen-reader operation, device performance and user
acceptance remain outside the completed evidence.

### Reading tool

The second task concerned typography, toolbar/navigation icons and small browser
identity in an existing local research-notes tool. The author retained the context,
note and outline structure, phone navigation and grey-green identity. Tiptap
3.32.0 continues to carry the document, selection, formatting, history and citation
mechanisms; Lucide 1.61.0 continues to carry functional icons. Store, storage tests
and fixtures are byte-identical to the input, including the v1 workspace contract.

Whole-to-detail observation found weak font-weight hierarchy in the baseline's
available fallback and an oversized, separate Georgia “Aa” control beside the
outline icon family. The author inspected Lucide's original icon/context demo,
the Tiptap Simple Editor's initial/focused/menu states, and Fontsource's actual
17px paragraph specimen. Tiptap's React template remained a design reference;
the existing vanilla-JS implementation was retained and adapted.

A same-content local trial compared serif reading/sans interface with an all-sans
direction. The actual adopted assets are Noto Sans SC Variable and Noto Serif SC
Variable 5.3.1, served locally as unmodified WOFF2 Unicode segments with OFL 1.1
notices. The default separates serif article/title text from interface controls;
the user can retain sans reading and choose 17/19/21px. These preferences stay
outside the v1 workspace export. Font readiness remeasures the title, while
style-only synthesis allows visible Chinese italic formatting without synthesized
weight.

Lucide paths and their coordinate system remain intact. Consistent line weight,
tool/navigation size, grouping and `ALargeSmall` replace the detached “Aa” treatment.
The native paragraph selector keeps its behavior. Phone overflow moves the same
command buttons into a second row, with Escape and focus return. A final semantic
adjustment removes `aria-pressed` from the changing next-action reading/editing
button; the body still exposes read-only state. The final full browser run and
failure/offline captures correspond to this revision.

The bounded original asset is a book/bookmark identity, with a 32-unit master,
16-unit optical favicon variant, and SVG/ICO/PNG delivery. Its in-app mark and
constructed 16/32px light/dark specimen were actually inspected. File responses,
declarations and synchronized document titles were checked separately. Native
browser tab chrome and favicon-cache behavior were not observed.

![Final desktop editor with retained context, article and outline relationships](evidence/v1.10.0/reading-after-desktop.png)

![Final phone editor with coordinated type, controls and labeled navigation](evidence/v1.10.0/reading-after-mobile.png)

The [phone baseline](evidence/v1.10.0/reading-before-mobile.png),
[same-content trial](evidence/v1.10.0/reading-type-trial.png) and
[constructed identity specimen](evidence/v1.10.0/reading-brand-size-specimen.png)
retain their different observation roles.

| Current-product check | Actual result |
|---|---|
| Original storage contracts | **10 tests passed** with the test source unchanged. |
| Browser flows | **16 checks passed**: local fonts/preferences, toolbar keyboard behavior, italic/undo/redo, draft-preserving discussion, citations/return, versions, v1 backup/import/recovery, reload, save states, mobile navigation and failure paths. |
| Layout | 1440×1000, 1280×800, 900×700, 390×844, 320×740 and a 390×500 short dialog; no document horizontal overflow in these checks. |
| Failure conditions | WOFF2 blocked for actual fallback rendering; real storage-error branch preserves input and exposes backup; final frames viewed. |
| Production and offline delivery | Build passed; the final self-contained file opened with network disabled, zero HTTP requests and no script error. |

The author viewed the ordered input-before/pending/saved frames, whose capture
brackets are recorded. This establishes the inspected progression together with
storage assertions, not frame rate or smoothness. The separate visual reviewer
opened **20 whole images and six detail crops**, reconciled every image hash with
runtime revision `7860bf3b9d0aa28d`, and found no visual blocker. It did not operate
the application or treat reported functional tests as facts proved by stills.

Font adoption has a measured delivery cost: the default first screen requests 26
local segments totaling 1,615,572 decoded resource bytes; the standalone file is
14,725,956 bytes because it embeds all segments. This is packaging/loading evidence,
not a network or device-performance benchmark. Real-device keyboards/IME, other
browser engines, OS scaling, assistive technology, native browser tabs and actual
long-reading preference remain unverified.

Both applications' source identities, exact adoption excerpts, conditions, checks,
independent image reviews and representative-image hashes are in the
[application evidence](evidence/v1.10.0/application-review.json). The temporary
products and their dependencies do not become installed skill dependencies.

## README publication review

The existing Markdown/native-host foundation and editable theme-aware artwork
continue to carry the public reading path. The new section explains normal-scale
whole-to-detail observation, its return to context and the temporal relationship.

The local Markdown-It/Chromium renderer exercised English and Chinese, light and
dark, at 390×844, 768×1024 and 1440×1000. A separate reviewer actually opened all
24 viewport/full-document images and 12 original-pixel crops of the changed
section. Full-document images were overview evidence. Crop geometry was checked
against an offline rerender using the same article dimensions and CJK fonts.

No blocking visual issue was found. The new hierarchy, emphasis, reading rhythm
and links remain visible under those conditions; Chinese glyphs render normally.
At 768px, an English paragraph ends with the short line “carry it.” and a Chinese
guide link wraps its last character. These are recorded as nonblocking typography
observations. At 390px the installation command uses its native horizontally
scrollable code container; its full text is not visible in the still frame.

Reviewed source SHA-256:

- English: `b56c861f06f32e944394dd274d60338b858c0f3b934a9c5d72594847327b9b2e`.
- Chinese: `ddd1637b08aed0834a9b358db770590270038ebbc1e29d61f8f5551a5a52f8fa`.

The image reviewer did not operate copy, links, horizontal code scrolling or
disclosure. The renderer exercised native text availability, image selection/alt,
disclosure and document overflow. Actual GitHub rendering is a separate exact-source
CI artifact and post-publication visual readback; the local result is an approximation.

## Engineering and release assurance

The standard Skills CLI 1.7.4 installed this skill in disposable projects for
requested Codex, Claude Code and OpenCode targets. It produced two actual copies,
verified all 29 files in each, and executed prepare, coverage-checker and resource
lookup helpers. This establishes installation and file integrity, not three host
model sessions. The restricted attempt could not reach npm or write its default
cache; a normal auto-reviewed retry with a temporary cache passed.

The read-only local preview initially could not launch Chromium inside the process
sandbox. An auto-reviewed retry ran the same renderer successfully. No capture
settings or assertions were weakened. Artwork, generated resource-map consistency,
local package validation and `git diff --check` passed during source integration.

After the application record was assembled, package validation, artwork and catalog
consistency, all **153 unit tests**, and `git diff --check` passed. The ten frozen
method files still match the application input byte-for-byte; the README hashes
also remain unchanged from the actual local visual review. The release build and
its four distributed assets use the final source, with exact-commit CI and remote
readback recorded by the version's workflow and Release.

Existing CI gates retain their scoped product, asset, content and temporal fixtures.
Their automatic success does not establish that all captured media were viewed or
that a real product's audience accepted its design. Publication requires the existing
cross-platform tests, source/version installation, README rendering and browser
fixture gates; the release procedure downloads and compares the expected assets
before publication. Post-publication GitHub screenshots are inspected separately
against the same README source identities.

## Research provenance and interpretation limits

The [source record](../skills/ui-spec/references/sources.md) adds dated primary
documentation observations for Atlassian optical spacing/type relationships and
Carbon icon/type pairing. These are documentation readings, not visual trials of
those systems or universal token prescriptions. The multiscale loop and selective
lenses synthesize the user's accepted methodology with the existing foundation.

Visible facts, professional interpretations, causal hypotheses, engineering
measurements and actual user response keep separate evidence. An enlarged crop
can explain an edge; normal-scale context determines its practical importance.
Sampled frames establish their observed states and relationships; continuous pacing
and runtime frame delivery need corresponding evidence. Product acceptance and
unobserved device, input or assistive-technology conditions remain explicit.
