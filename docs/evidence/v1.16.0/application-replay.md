# Reconstructing the bounded application observation

This is a traceable local study, not an installed positive-example corpus.
The already prepared input is identified by commit
`7d276ee220aa57442e43096a178964359ae65e13` in this repository. That commit's
`.development/craft-study.jsx` is the task wrapper and
`.github/workflows/visual-craft-development.yml` records the exact source and
build procedure. The original successful run is 40536750577, artifact 12747644228.
The original artifact hash is recorded in application-review.json.

The build uses React/ReactDOM 19.2.0 and esbuild 0.25.10, and exact SpotlightCard
and TiltedCard sources from React Bits revision
`e12c22192ac7b4b452c5e2feb9b586d74765d696`. Read the source's actual license before
acquiring or using it. Raw components and the compiled dependency bundle are
not redistributed here. The source identity record retains file hashes; the
working wrapper, source paths and build settings remain discoverable at the
fixed commit, without relying on mutable branch names.

`application-host.css` is the host adaptation actually used in the final study.
`application-capture-driver.txt` preserves the executed capture script as an
execution record, not a new tool or required dependency. In a permitted local
working directory, the original input's dist files plus that CSS and a Chromium/
Playwright installation allow the same offline fixture operations. The driver
assumes its sibling `dist` directory and `/usr/bin/chromium`; adjust only explicit
environment paths when reproducing. It changes an exact wrapper query-expression
for each condition, not the vendor mechanism. Preserve content, settings and
source identity when comparing observations.

The captured sequences are sparse samples, not proof of natural-time smoothness.
The sample's 280ms delay is not a measured network response. Host emulation does
not establish physical-device interaction, production behavior or full
localization. Full Agent tests have separate inputs and status.
