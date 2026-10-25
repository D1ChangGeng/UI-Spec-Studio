# Content design in a real UI state

A small bilingual research-note editor used to test **meaning → content distribution → UX writing → typographic composition → actual interaction and feedback**. The scenario is a browser-local demonstration, not a production application or an independently measured user study.

## User task and source of truth

A person wants to capture a research question, optionally note its context, and return to it in the same browser. The primary action is **Save note**. Actual persistence is provided by `localStorage`, whose success or failure determines the visible status. The UI identifies this boundary in both languages. Real service accounts, collaboration, server storage and external research content are outside this fixture.

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
| Failure | 当前无法保存这份笔记。输入内容仍在页面中。 | This note could not be saved. Your text is still here. | Explains the unsuccessful action and retained draft | `#retry`, local failure flag |
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

Open `http://localhost:8080/`, switch Chinese/English and light/dark themes, enter a title, save, reload, then exercise missing-title and simulated-failure cases in **Preview state controls**.

The automated browser runner executes from the repo root:

```bash
python tools/validate_content.py --output-dir content-evidence
```

It captures supported content states and actual viewports, checks locale-specific text and field associations, verifies browser persistence, and compares the visible status with the simulated storage boundary. Actual screenshots and the report provide the scoped evidence. Independent end-user comprehension and a production API remain separate acceptance tasks.
