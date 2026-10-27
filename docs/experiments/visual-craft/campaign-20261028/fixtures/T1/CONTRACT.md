# Business and test interface

Immutable `src/domain.js`: loadThreads/saveThreads, INITIAL_THREADS, SOURCES, requestAnswer(question,{signal,attachments}). Each attachment needs a `name`. Use actual asynchronous results. Do not emulate fixture results separately.

Set `window.__fixtureMode` to `slow`, `error`, `long` or `normal` from a test to control the next response. Query `?response=slow|error|long` also initializes a scenario. Stop/route changes require AbortController or equivalent stale-result protection.

Stable `data-testid` hooks: `new-thread`, `thread-t-seed`, `thread-t-quiet`, `thread-${id}` for other histories, `theme-toggle`, `composer` on the textbox, `send`, `file-input` on an input[type=file], `attachment` on each attached item, `remove-attachment-${index}`, `messages` on the reading area, `assistant-message`, `user-message`, `pending`, `stop`, `error`, `retry`, `source-s1/s2/s3` on source-open controls, `source-dialog` on visible dialog, `source-close`.

Source-open controls can repeat per answer. A narrow viewport may put history in a drawer: expose `history-toggle` on its trigger if used. All controls need meaningful accessible names; test hooks do not replace them. UI copy can be English; fixture meaning must be retained. `t-seed` has three source records; `t-quiet` is the second conversation. LocalStorage key is exported from domain.
