# Evidence and reproduction

All browser interactions used the actual app at http://127.0.0.1:8739/app/ through a local HTTP server. Each test creates an isolated Chromium context. Storage checks use real browser localStorage across reload.

Environment supplied by TOOLING.md:

- Python: `/workspace/scratch/43b440780c87/test-env/bin/python`
- Browser: `/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell` (Chrome 143)
- Fontconfig: `/workspace/scratch/43b440780c87/preview-fontconfig.xml`
- Main viewports: 1440×900 and 390×844, DPR 1. An additional 390×500 check exercises reduced available height.

Run from the cell directory with the local server started:

```bash
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/test_app.py
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/test_continuity.py
```

## Records

- `test-results.json` and `test-run-final.log`: latest 29-assertion functional run, including console/network observation.
- `continuity-results.json` and `continuity-run.log`: latest 10-assertion reading/resume/history run; screenshot capture start/end timestamps are recorded.
- `test-results-01-initial-failure.json`: genuine initial startup failure; paired broken source retained.
- `test-results-03-scroll-failure.json` and `test-results-04-scroll-still-failing.json`: original observed scrolling checks retained, including failed observations.
- `scroll-diagnostic.log`: targeted state measurements that revealed the initial non-overflowing scroll setup.
- `test_app_original_scroll_setup.py`: original test retained before strengthening the setup to wait for overflow.
- `test-results-05-stable-nodes.json`: intermediate stable-paragraph regression before the strengthened test setup.
- `reference-*.png`: supplied reference rendered locally, then actually viewed.
- `final-*.png`: current desktop/mobile compositions captured by the continuity run.
- `continuity-01-reading-older.png` and `continuity-02-new-content-below.png`: ordered views while content grows below a retained reading position.

Screenshots are factual captures. The corresponding views were inspected separately with the image viewer; writing a screenshot does not itself establish visual review. This session used stills and ordered samples, not full-speed video playback or human usability research. See `../DESIGN.md` for perceptual observations and limits.
