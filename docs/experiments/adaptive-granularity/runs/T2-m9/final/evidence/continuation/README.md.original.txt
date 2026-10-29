# Source-reading continuation evidence

Run from the assigned cell while the local HTTP server is listening on 127.0.0.1:8739:

```bash
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/continuation/check.py
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/continuation/follow_check.py
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/continuation/regression_check.py
```

`results.json` contains the final focused assertions and capture start/end timestamps. `follow-results.json` covers explicit following with the dock open, real wheel interruption, keyboard citation activation, 1280px reflow anchoring and the sticky phone Back control. `regression/test-results.json` exercises inherited conversation and persistence behavior in a separate browser context.

`app-before.js`, `styles-before.css` and `index-before.html` preserve the prior implementation. Intermediate runs are retained with numbered names. The recovery-control visual finding is preserved in `07-failure-before-visibility-fix.png`, with its corresponding source snapshot and pre-fix results. Captures are separate from actual visual observations documented in CONTINUATION-DESIGN.md. No full-speed video playback or physical-phone/screen-reader validation was performed.
