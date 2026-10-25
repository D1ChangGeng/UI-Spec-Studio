# 1.6 review: content and complete product experience

Reviewed on 2026-10-25. The published baseline is v1.5.0, commit `b65941a2e3f644716a4ed510e01ea88ecbcf8439`. Work resumed from the existing unpublished content-design branch at `7e842e12b372fffe89385a57689177bae56ff127`. Its files and complete Git tree were checked against the repository before the remaining changes were applied. The release incorporates that branch and the completion work described here.

## Accepted capability and responsibilities

Content Design, UX Writing and Typography participate in product understanding, information distribution, actual wording, visual composition, interaction and verification. The working relationship is **user need and product facts → content responsibility and timing → mature-product research → wording and tone → rendered integration → observed outcome**. Content can change structure, components and the journey as new evidence becomes available.

The complete experience model coordinates nine design dimensions: product and interaction model, visual direction, visual assets, content and typography, layout and spatial composition, components and states, motion continuity, performance, and ongoing operation. The [experience guide](EXPERIENCE-QUALITY.md) maps each dimension to its responsible reference and explains how project mechanisms transfer with their applicable conditions.

| File or group | Responsibility in this release |
|---|---|
| `SKILL.md` | Establish the content capability, nine-dimension scope and eight common readings |
| `content-design.md` | User vocabulary, information placement, voice/tone, actual copy, complete messages, typography, localization and maintained content |
| `analysis.md` | Product objects, real choices, content sources and the dimensions that affect the current task |
| `workflow.md` | Carry those decisions through Init, optional Shape, Iterate, Audit and Finish |
| `principles.md` | Compose actual text and assets with hierarchy, optical weight and full dynamic space |
| `component-sourcing.md` | Research mature product and language patterns; preserve useful foundations and adoption evidence |
| `interaction-and-variants.md` | Complete states, action relationships, motion reversal, scrolling, growth and responsive repeated work |
| `verification.md` | Inspect actual output; distinguish editorial, visual, interaction, timing, authority and user evidence |
| `integration.md` | Valid preparation/cache boundaries, real outcomes, content inheritance, roles and partial batch recovery |
| Records, source maps and bilingual guides | Keep consequential decisions, sources, approved copy and observed scope available for continuation |

The eight common references remain complementary. Repeated explanations were consolidated in their responsible sections; the existing 144 KiB combined-content check remains unchanged. Runtime instructions stay in English, with bilingual introductions. Existing workflow names, host authority and optional-helper boundaries remain intact.

## Content fixture: observed problems and repairs

The [bilingual research-note editor](../examples/content-review/README.md) uses actual browser-local storage. Its wording explicitly identifies that boundary. The review connected each important message to the operation it describes:

- An unavailable read is distinct from an empty collection. Unknown or malformed saved content is retained until supported recovery succeeds; the editor does not silently overwrite it.
- Clearing reports success only after removal succeeds. A failed removal keeps useful input and offers the matching retry.
- A save captures the submitted version. If the user edits during the write, the result distinguishes the saved version from the newer unsaved draft.
- Repeated submission preserves the in-flight intent; a clear action cancels a pending local write so deleted data cannot reappear later.
- Language and theme changes preserve the current task and produce the correct current message. A disappearing retry action leaves focus on a usable input within the viewport.
- The language control's accessible name contains its visible label. Long saved titles wrap in the result region.
- Actual image inspection identified an overlong English input example and a two-character Chinese orphan line in the introduction. Both strings were shortened without changing their task meaning and the affected rendering was checked again.

Storage read/write/remove failures are injected at the real browser Storage boundary. Controlled-clock cases establish ordering during a pending write; the authored delay is not a performance measurement. The fixture's single-note, browser-local contract is explicit.

## Executed local checks

Local browser runs used Playwright 1.57.0 and Chromium 143.0.7499.0 over HTTP, with Noto CJK fonts available for the declared Chinese content. The native browser storage path was used. Reports identify the renderer and individual observations.

| Evidence | Executed scope and result |
|---|---|
| Unit suite | 149 tests passed, including the existing common-reference density limit |
| Content browser runner | 39 check groups passed; actual storage verified; 53 viewport/full-document captures; no page errors or external requests |
| Content conditions | Chinese/English × light/dark × 390, 768, 1280 and 1920 CSS-pixel widths; additional 320px text-spacing/reflow and meaningful state captures |
| Content visual inspection | All 53 captures opened across the review team; wording fit, hierarchy, long content and recovery visibility reviewed separately from assertions |
| Local README preview | 12 language/theme/width conditions, each with viewport and full-document captures; all 24 images opened; no blocking composition or reading issue observed |
| Existing product scenario | 18 checks and 28 captures passed; actual local persistence verified |
| Existing asset scenario | Eight views and eight state checks passed, including actual files, fallbacks, themes and motion policy |

The README preview uses Markdown-It and a GitHub-like stylesheet. It establishes local rendering evidence; the main-branch publication job separately exercises the actual GitHub host. Existing product and asset scenarios provide regression observations in their declared scope. Their original product approval and specialist production claims remain separate.

## Independent forward application

A fresh agent context received the skill path and the following task, without the preceding implementation discussion or suggested solutions. It read the complete common references and the relevant integration guidance, then researched primary product and technical sources.

> 请使用 UI Spec Studio 的 ui-spec 方法处理下面的产品设计任务。只做设计分析，不修改仓库或其他文件，不操作真实服务。
>
> 我们正在做个人使用的图片整理工具。用户会一次选 1–60 张图片，预览裁切并导出；经常连续换图，现在切换时要等上一张的预览完成。图片名和备注可能很长。中文和英文都要支持，可在手机或桌面使用，支持浅深主题。当前内部状态叫 queued / worker_accepted / encoded / persisted，偶尔请求超时但任务其实仍在后台运行。设置页可保存共用水印，单张图片也可修改水印；用户常常希望对筛选出的图片统一应用某项修改。
>
> 请给出可以交给设计和前端实施的一轮方案：主要界面与操作安排、关键中英文文案、状态及恢复行为、性能处理思路和验收方法。明确缺少哪些真实业务依据；其他可逆选择自行决定。不要把技术状态名称直接展示给普通用户。

The task-local prompt also requested about 1,800 Chinese characters and references actually consulted. Observed decisions included:

| Task concern | Actual proposal |
|---|---|
| Product model and continuity | An object editor with a supporting collection; preserve selection, crop draft and return position; separate the active image from batch selection |
| Long content and variants | Reveal full names while preserving extensions, expand long notes, and change desktop/mobile composition without changing the task model |
| Watermark ownership | Shared, custom and none states; explicit restore-inheritance behavior; freeze the export's template version so later edits do not silently change an in-progress result |
| Batch work | Persist selected IDs across filtering, disclose hidden selected items, apply only chosen fields and retain completed items after partial failure |
| Truthful wording | Parallel Chinese/English actions and outcomes; show an unknown timeout as unknown; query the original task before a retry can duplicate it |
| Performance method | Immediate selection feedback, a usable low-resolution preview, current/neighbor preparation with bounded work, and cache identity tied to image and editing revisions |
| Verification boundary | Separate feedback, usable preview and available export timings; identify provisional timing budgets as needing target-device calibration |

The output consulted [Adobe Lightroom](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/develop-module-options.html) and [React Spectrum](https://react-spectrum.adobe.com/v3/ActionBar.html) for editing and selection, [MDN](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) for cancellation, [web.dev](https://web.dev/articles/optimize-inp) for input responsiveness, and W3C for [reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) and [status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html). It identified missing format/device constraints, task-query and idempotency support, cancellation semantics, output limits and retention rules as product facts to establish.

This is one observed planning application. It supports the transferability of the written method to a different task. It does not establish implemented image-tool behavior, production performance, independent user comprehension, comparative model quality or reliability across hosts. Proposed timing budgets remain proposals.

## Release assurance and limits

Package/link validation, generated catalog/art checks, reproducible packaging and standard Skills CLI installation accompany the unit and browser gates. CI executes the declared Python/OS matrix, checks the exact committed remote source and actual GitHub README rendering, and requires successful test, installation, publication and scenario jobs before release. The publication tool verifies downloaded asset bytes before publishing the release; final handover reads back the tag, release and workflow result.

The [release workflow](../.github/workflows/validate.yml), [evaluation model](EVALUATION.md) and [release notes](releases/v1.6.0.md) identify the reproducible commands and evidence boundaries. Product-specific business policies, service calls, real-user understanding and performance gains require the corresponding product evidence. Source-guided methods and this local fixture do not certify those separate outcomes.
