# ATELIER — studio field-research workspace

Create a finished professional workspace for ATELIER, an independent studio conducting field research across regions. The application is already populated with twelve projects. People use it to understand the studio's workload, locate a project, review upcoming fieldwork, change a project's status, and add research notes.

Give ATELIER a distinctive editorial and spatial identity that remains convincing throughout actual daily work. Bring high visual craft to the populated Overview, Projects, and Schedule views; the information-heavy project detail; and ordinary controls, feedback, and empty states. Make the workspace feel like one considered product. Choose the visual direction and interaction presentation yourself.

The result must be real, runnable software. The starter is deliberately plain and may be replaced. Keep the existing business domain, data, and public behavior intact. `src/domain.js` is immutable: import its public functions rather than rewriting its seed data or persistence rules. UI code, styling, and presentation structure may change. Do not add a network service or require an account, secret, or backend. Preserve the behavior-oriented `data-testid` hooks in `CONTRACT.md`; they do not prescribe a visual layout or component library.

Support selectable light and dark themes, with a remembered choice. Make the full workspace usable at viewport widths of 390, 900, and 1440 CSS pixels. Support keyboard operation; a project detail must behave as a dialog, close on Escape, and return focus to the control that opened it. Respect reduced-motion preferences. Long project descriptions and notes must remain readable and usable.

## Ten business acceptance requirements

1. **Overview totals.** On a clean first load, Overview is populated and displays 12 projects, a total budget of **USD 585,000**, and status counts of **4 Planned**, **5 In progress**, and **3 Review**. Summary numbers describe the full workspace and remain correct when the project list is filtered.
2. **All projects.** Projects shows all twelve seeded projects when search is empty and the status filter is All. Keep every project's identity, title, owner, region, budget, dates, description, methods, and original note intact.
3. **Search.** Searching Projects for the exact title **Harbor Night Markets** returns only `PRJ-001`; clearing the search restores all twelve projects when no status filter is active. Search supports title, owner, or region without case sensitivity.
4. **Status filter.** Filtering Projects to Planned on the original state shows exactly `PRJ-003`, `PRJ-007`, `PRJ-009`, and `PRJ-012`. Clearing the filter restores all twelve projects when search is empty.
5. **Schedule.** Schedule contains all twelve projects and exposes each project's correct start and due dates. Its information comes from the same project state as the other views. The schedule presentation is your choice.
6. **Correct, accessible detail.** Opening Harbor Night Markets shows `PRJ-001`, Maya Chen, East Asia, USD 48,000, start 2026-10-05, due 2026-11-13, its full description, methods, and original note. The detail supports keyboard operation, closes on Escape, and restores focus to its opener.
7. **Status update across views.** Change Harbor Night Markets from In progress to Review. The detail, Projects, Schedule, and Overview must agree. Overview then shows 4 Planned, 4 In progress, and 4 Review; its total budget remains USD 585,000 and project count remains 12.
8. **Save a note.** Add **Interview synthesis ready for partner review.** to Harbor Night Markets. Show the new note and its author, You, alongside the preserved original note. Closing and reopening the detail must retain the note. Reject an empty or whitespace-only note. Notes may contain up to 2,000 characters.
9. **Reload persistence.** After the status change and note addition above, reload the page. Harbor Night Markets must still be in Review, both notes must remain, and the summaries must still reflect the change. Keep the other eleven projects' data intact.
10. **Responsive themes.** At widths 390, 900, and 1440, navigation, search, filters, and project detail remain reachable and operable without page-level horizontal overflow. Both selectable themes must visibly apply throughout the workspace and dialog. The selected theme survives a reload. Under reduced motion, the same controls and dialog still work, with nonessential motion reduced or removed.

## Fixed fixture facts

All budgets are in USD. Original status budget totals are Planned **201,750**, In progress **254,500**, and Review **128,750**. Each project begins with one authored research note. The complete descriptions, methods, and note text are in `src/domain.js`.

| ID | Title | Owner | Region | Original status | Budget | Start | Due |
|---|---|---|---|---|---:|---|---|
| PRJ-001 | Harbor Night Markets | Maya Chen | East Asia | In progress | 48,000 | 2026-10-05 | 2026-11-13 |
| PRJ-002 | Alpine Public Rooms | Jonas Weber | Europe | Review | 36,500 | 2026-09-14 | 2026-10-30 |
| PRJ-003 | Delta Water Stories | Amara Okafor | West Africa | Planned | 62,000 | 2026-11-02 | 2026-12-11 |
| PRJ-004 | Transit After Hours | Luis Ortega | North America | In progress | 54,500 | 2026-10-12 | 2026-11-20 |
| PRJ-005 | Courtyard Commons | Noor Haddad | Middle East | Review | 41,000 | 2026-09-21 | 2026-11-06 |
| PRJ-006 | Coastal Repair Cultures | Sofia Martins | South America | In progress | 58,750 | 2026-10-01 | 2026-11-27 |
| PRJ-007 | Northern Light Diaries | Erik Solberg | Northern Europe | Planned | 32,750 | 2026-11-09 | 2026-12-04 |
| PRJ-008 | Everyday River Crossings | Priya Raman | South Asia | In progress | 47,250 | 2026-10-19 | 2026-12-18 |
| PRJ-009 | Desert Listening Posts | Salma Benali | North Africa | Planned | 39,500 | 2026-11-16 | 2026-12-18 |
| PRJ-010 | Shared Kitchen Atlas | Nico Rossi | Southern Europe | Review | 51,250 | 2026-09-28 | 2026-11-09 |
| PRJ-011 | Market Street Futures | Ada Brooks | Oceania | In progress | 46,000 | 2026-10-26 | 2026-12-07 |
| PRJ-012 | Forest Edge Exchanges | Elena Petrova | Eastern Europe | Planned | 67,500 | 2026-11-23 | 2026-12-21 |

## Run

Dependencies are supplied by the shared runtime through the local `node_modules` symlink. Do not change the shared dependencies. From this project directory, run `npm run dev -- --port <assigned-port>`. `npm run build` creates a production build. Use only your assigned project directory and port.

`CONTRACT.md` documents the public domain API and UI hooks. `acceptance.json` records the ten business checks without prescribing a visual solution.
