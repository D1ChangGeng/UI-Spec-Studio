# ATELIER fixture contract

## Immutable business domain

Keep `src/domain.js` byte-for-byte unchanged. Its initial project objects and nested values are deeply frozen. UI code may be replaced. The domain stores only permitted project edits—status changes and appended notes—and always restores all other metadata from the seed.

| Export | Contract |
|---|---|
| `WORKSPACE_NAME` | `ATELIER` |
| `STATUSES` | `Planned`, `In progress`, `Review`, in that order |
| `CURRENCY` | `USD` |
| `INITIAL_PROJECTS` | Twelve deeply frozen project records, each with one original note |
| `STORAGE_KEY` | `atelier-workspace-t2-v1` |
| `THEME_STORAGE_KEY` | `atelier-theme-t2-v1` |
| `createInitialState()` | Fresh mutable state: `{ schemaVersion: 1, projects: [...] }` |
| `loadState(storage?)` | Restore permitted edits from localStorage; invalid or absent saved data falls back to the initial state |
| `saveState(state, storage?)` | Save normalized permitted edits; returns `true` on success, `false` if storage is unavailable |
| `getProjectById(state, id)` | Return the project or `null` |
| `selectProjects(state, { query, status }?)` | Match title, owner, or region case-insensitively; combine with status; use `All` for no status constraint |
| `getScheduleProjects(state, filters?)` | Select projects and sort by due date, then ID; presentation may arrange them differently |
| `getWorkspaceSummary(state)` | Return `{ totalProjects, totalBudget, statusCounts, budgetByStatus }` over the full workspace |
| `updateProjectStatus(state, id, status)` | Return new state with one status updated; reject unknown IDs or statuses |
| `addProjectNote(state, id, body)` | Return new state with a note appended; trim text; require 1–2000 characters; set author `You`, a unique ID, and an ISO timestamp |
| `loadTheme(storage?)` | Return saved `light` or `dark`, defaulting to `light` |
| `saveTheme(theme, storage?)` | Persist `light` or `dark`; return a success boolean |

The optional `storage` argument supports any object with `getItem` and `setItem`. It exists for isolated verification, not a separate network service. To reset a browser fixture, remove only the two named keys and reload. A production UI need not expose a reset control.

## Stable UI hooks

Preserve these `data-testid` values. They identify behavior, data, or state; they do not require the starter's layout, styling, DOM element types, or component choices. Custom widgets must expose equivalent accessible controls and values. Inactive view content must not create duplicate active hooks. `${id}` below means an exact project ID such as `PRJ-001`.

| Hook | Meaning and expected behavior |
|---|---|
| `app-shell` | Application root; its `data-theme` is `light` or `dark` |
| `theme-toggle` | Accessible control for choosing the other theme; accessible name identifies the destination theme |
| `nav-overview` | Show Overview; indicate the active view accessibly |
| `nav-projects` | Show Projects |
| `nav-schedule` | Show Schedule |
| `overview-view` | Active Overview project collection |
| `projects-view` | Active Projects collection |
| `schedule-view` | Active Schedule project collection |
| `overview-summary` | Full-workspace summary, independent of search and filter |
| `summary-total-projects` | Project count, initially 12 |
| `summary-total-budget` | Total USD budget, initially 585000; formatting may vary |
| `summary-planned-count` | Full-workspace Planned count, initially 4 |
| `summary-in-progress-count` | Full-workspace In progress count, initially 5 |
| `summary-review-count` | Full-workspace Review count, initially 3 |
| `status-chart` | A populated graphical representation of the status distribution; presentation may change |
| `search-input` | Editable project search text; title, owner, and region are searchable |
| `status-filter` | Status choice: All, Planned, In progress, or Review |
| `clear-filters` | Clear both query and status filter |
| `results-count` | Visible number of matching projects and total workspace count |
| `empty-state` | Explanation when the active view has no matches |
| `project-item-${id}` | One project in the currently active view |
| `project-open-${id}` | Keyboard-operable control opening that project's detail |
| `project-title-${id}` | Exact seeded project title |
| `project-status-${id}` | Current status in the active view |
| `schedule-start-${id}` | Exact start date; expose ISO date in `datetime` or `data-date` |
| `schedule-due-${id}` | Exact due date; expose ISO date in `datetime` or `data-date` |
| `project-detail` | Modal project detail with an accessible name, keyboard containment, Escape dismissal, and opener focus restoration |
| `detail-title` | Exact title of the open project |
| `detail-close` | Close the detail |
| `detail-summary` | Full project description |
| `detail-id` | Exact project ID |
| `detail-owner` | Exact owner name |
| `detail-region` | Exact region |
| `detail-budget` | Exact USD budget, formatting may vary |
| `detail-start` | Start date with ISO `datetime` or `data-date` |
| `detail-due` | Due date with ISO `datetime` or `data-date` |
| `detail-status` | Editable project status; selection updates shared state immediately |
| `detail-notes` | Collection of the project's original and appended notes |
| `project-note` | One note, including body and author; this hook intentionally repeats inside `detail-notes` |
| `note-input` | Editable note body, up to 2000 characters |
| `note-save` | Save a nonempty trimmed note; must not append an empty note |
| `detail-message` | Accessible feedback for a note save or status change |

Keep the current theme reflected on `document.documentElement.dataset.theme` as well as `app-shell` so browser verification can observe it. A changed attribute alone is insufficient: the selected theme must visibly apply to the product and its dialog.

## Initial facts used by acceptance

- 12 projects; total budget USD 585,000.
- Planned: 4 projects, USD 201,750; IDs PRJ-003, PRJ-007, PRJ-009, PRJ-012.
- In progress: 5 projects, USD 254,500; IDs PRJ-001, PRJ-004, PRJ-006, PRJ-008, PRJ-011.
- Review: 3 projects, USD 128,750; IDs PRJ-002, PRJ-005, PRJ-010.
- PRJ-001: Harbor Night Markets, Maya Chen, East Asia, USD 48,000, start 2026-10-05, due 2026-11-13.
- PRJ-001 original note: `Vendor interviews are scheduled for the first two evenings.`
- After PRJ-001 changes to Review: Planned 4 / USD 201,750; In progress 4 / USD 206,500; Review 4 / USD 176,750. Total projects and budget remain unchanged.
- Acceptance note: `Interview synthesis ready for partner review.`

All twelve exact records are in `src/domain.js` and the table in `TASK.md`. Do not substitute different projects or alter fixture facts to fit the design.
