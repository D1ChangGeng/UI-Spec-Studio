# Content design in a real UI state

A small bilingual research-note editor used to test **meaning → content distribution → UX writing → typographic composition → actual interaction and feedback**. The scenario is a browser-local demonstration, not a production application or an independently measured user study.

## User task and source of truth

A person wants to capture a research question, optionally note its context, and return to it in the same browser. The primary action is **Save note**. A single note is held in `localStorage`; successful reads, writes and removals determine the visible content and feedback. An unavailable or malformed stored record has its own recovery state and is preserved until an explicit successful action. The UI identifies this boundary in both languages. Real service accounts, collaboration, server storage and external research content are outside this fixture.

The visible structure makes these content decisions explicit: the page heading orients; the persistent form label identifies input; the hint communicates scope; the action names the operation; feedback distinguishes pending, saved and unavailable; the adjacent recent-note area responds to real browser state rather than placeholder marketing copy.

## Content decision and visual placement

| Surface / role | Chinese wording | English wording | Why and when it appears | Source and actual location |
|---|---|---|---|---|
| Main heading | 把研究线索整理成笔记 | Turn a research lead into a note | Orient the primary task at first encounter | Authored fixture voice; `#main-title` |
| Title label / hint | 笔记标题 / 用一句话写清想研究的问题 | Note title / Name the question you want to investigate | Input role stays visible while typing | `#note-title` and `#title-hint` |
| Action | 保存笔记 | Save note | Describes the actual local save | `#save`, storage boundary in `app.js` |
| Required-field error | 填写笔记标题后再保存。 | Add a note title before saving. | Appears at the field on invalid submit and focuses it | `#title-error`, `aria-describedby`, `aria-invalid` |
| Pending | 正在保存到此浏览器… | Saving in this browser… | Immediate acknowledgment while writing | `#state-message` |
| Success | 笔记已保存在此浏览器。 | Note saved in this browser. | Appears only after the local write returns normally | `showStatus('saved')` |
| Failure | 当前无法保存这份笔记。输入内容仍在页面中。 | This note could not be saved. Your text is still here. | Keeps the prior saved result and current draft distinct | `#retry`, a native or simulated write failure |
| Editing during a write | 上一版已保存。当前修改仍需再次保存。 | An earlier version was saved. Save again to keep your new edits. | The submitted snapshot was written while the user continued typing | `currentRecord()`, captured write snapshot and `#state-message` |
| Read unavailable | 暂时无法读取已保存的笔记… | Saved notes could not be read… | Explains uncertainty, preserves the draft and offers a read retry before replacing stored content | `readStored()`, `#retry` and `#recent-card` |
| Clear failed | 未能清除本地演示数据… | Local demo data could not be cleared… | Reports the failed removal and keeps the current input for recovery | `clearStored()` and `#retry` |
| Secondary outcome | 最近保存 | Recently saved | Displays confirmed saved data to support return | `#recent-card` |

Brand voice is direct, measured and task-oriented; tone becomes more explanatory for limitations and recovery. Chinese and English are natural parallel formulations rather than character-for-character translations. The typography uses a display heading and a readable system UI face; full content controls the width, height and response at small viewports.

## Source-informed methods

- [GOV.UK content design](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design/): ask what someone needs to know or do, and place information where it serves the task.
- [Microsoft UI writing](https://learn.microsoft.com/en-us/windows/apps/design/style/writing-style): lead with the important message, use meaningful action verbs and constructive feedback.
- [IBM Carbon content foundations](https://www.carbondesignsystem.com/building-blocks/foundations/content): stable terminology and context-appropriate language.
- [W3C labels and instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions) and [error identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification): preserve explicit, understandable form labels and errors.

Sources were reviewed for this methodology on 2026-10-25. Layout, wording, theme and runtime code are original work for the fixture. All sample content is fictional and explicitly identified as local demonstration data.

## Run and inspect

From the source root:

```bash
python -m http.server 8080 --directory examples/content-review
```

Open `http://localhost:8080/`, switch Chinese/English and light/dark themes, enter a title, save and reload. Each navigation initializes Chinese/light; switching either control during a task preserves the draft and current result.

In **Preview state controls**, exercise a write failure or a one-second write delay. Edit during the delay to compare the submitted snapshot with the current draft. Clearing the local demo data cancels a pending write; a successful removal clears the editor and saved result together. The delay is authored to expose the pending state, not a measured storage or service latency.

Read and removal failures are injected at the real Storage boundary by the browser runner. A read failure remains visibly different from an empty note collection. Retrying a read keeps an already edited draft; retrying any operation leaves keyboard focus on a usable input when its recovery button disappears. Malformed persisted data remains intact until the explicit clear action succeeds.

The automated browser runner executes from the repo root:

```bash
python tools/validate_content.py --output-dir content-evidence
```

The runner checks Chinese and English, both themes and four CSS viewports (390×844, 768×1024, 1280×800 and 1920×1080). Its report lists each viewport or full-document capture separately and records the browser version and exact checks. The exercised paths include:

- Visible and accessible names, required-field errors, supporting-text contrast, saved long content and reflow.
- Actual writes and reload restoration, simulated and native write failures, removal failure/retry, native read failure and malformed-data recovery.
- Input retention, language/theme changes during pending work, a saved snapshot with a newer unsaved draft, repeated submission and cancellation through clearing.
- Keyboard entry, recovery focus, reduced-motion styling and a 320px layout under text-spacing overrides.

Race cases use Playwright's controlled clock so the outcome does not depend on test-machine speed. They establish state ordering, not a performance score. The optional `--in-memory` mode uses a simulated storage object and reports native persistence and startup-read checks as unverified. The default HTTP run uses actual browser storage, with explicitly injected faults for recovery cases.

Passing assertions and producing screenshots establish their stated mechanics. Open the captured images to judge composition and reading rhythm. Independent end-user comprehension, production APIs and real-device/service performance retain their own evidence.
