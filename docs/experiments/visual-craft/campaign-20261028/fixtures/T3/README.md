# Margin input fixture

A small local Vite + React input project for the source-sheet task described in `TASK.md`. The accepted notebook shell, fictional source records, delayed request API, explicit note persistence, and public interaction hooks are already provided.

```sh
npm run dev -- --port 5173
npm run build
```

Dependencies are supplied by the shared `node_modules` symlink in this environment. No backend or external credentials are needed. The production build uses a relative base path.

Read `TASK.md` for the requested work, `CONTRACT.md` for fixed input behavior and interaction hooks, and `acceptance.json` for the ten requirements in structured form.

The source sheet is deliberately a starter. It already opens the correct source, fetches with cancellation, switches sources, retries failures, provides an expanded size, edits and saves notes, contains keyboard focus, and closes with focus return. Its drag handle is initially decorative, its mode changes are immediate, and dismissal has no transition. Those are part of the focused redesign task.

The surrounding notebook is accepted. The only requested sidebar change is the existing Saved → Library label in `src/navigation.js`.
