# README as a screen-based UI SPEC

## Purpose and experience contract

**Surface:** the GitHub repository landing page, delivered as bilingual GitHub-flavored Markdown. The primary reader arrives to assess whether UI Spec Studio fits a design task and to run the first useful Agent instruction. A returning reader finds operation/installation details; a maintainer follows source and verification links.

**Primary reading path:** recognize the purpose → copy the install command → give an Agent the first task → understand the resource-led method → review examples and assurance. Deeper methodology remains linked by role, and maintenance tools use disclosure.

**Desired identity:** a calm editorial design practice with an explicitly research-led foundation. Warm paper/dark evergreen and restrained rust connectors are retained from the established project treatment; native GitHub text remains the main explanatory medium. The illustration is a visual expression of a process rather than a product screenshot or external performance claim.

## Mature-source research and selection

The task is a **publication/reading interface**, so GitHub Markdown and mature README information architectures are the appropriate highest reuse level. A web application shell or React component library would replace a host that already provides navigation, selection, links, copyable code and scrolling. Design-pattern reuse is more valuable than imported UI runtime code for this medium.

The following publicly accessible primary sources were inspected for their specific reusable relationships on 2026-10-25:

| Candidate and source | Useful design mechanism | Adoption decision | Source to implementation |
|---|---|---|---|
| [Vercel Skills CLI README](https://github.com/vercel-labs/skills/blob/main/README.md) | A clear tool premise followed by one runnable install command, focused examples and deeper documentation links | **Selected:** information architecture; technique transfer | First-use section near the top; host-specific details later in [`README.md`](../../README.md) and [`README.zh-CN.md`](../../README.zh-CN.md) |
| [Typst README](https://github.com/typst/typst/blob/main/README.md) | An actual visual example coupled with an explanation in readable text | **Selected:** demonstration pattern; technique transfer | Editorial process artwork plus native explanation and decision table |
| [GitHub Markdown and `<picture>` guidance](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) | Semantic document flow, copyable code and theme-responsive images with alt text | **Selected:** direct host capability | Native headings, tables, links, code and `<picture>` with four local SVG variants |
| [Astro README](https://github.com/withastro/astro/blob/main/README.md) | Banner-led identity, immediately actionable install and deeper documentation | **Considered:** the hero-plus-entry balance transfers; the extensive package directory belongs to its monorepo context | Supported the shorter reading path and a single illustration |
| [shadcn/ui README](https://github.com/shadcn-ui/ui/blob/main/README.md) | Brief positioning, large demonstration image and direct documentation route | **Considered:** concise identity and one clear picture; its component-gallery priority belongs to its product | Helps bound the visual illustration and leave product UI demo in a linked study |
| Existing UI Spec Studio editorial SVGs, [`readme_art.py`](../../tools/readme_art.py) | Retained art direction, editable geometry, light/dark variants and independent narrow treatment | **Selected:** in-place adaptation at the asset layer | New theme-aware plates: sources → evaluation → published document |

**Reuse granularity:** GitHub-native publishing surface and document-level reading organization, combined with selected example patterns. **Adoption mode:** structural/design technique transfer with project-authored editable artwork; native GitHub Markdown requires no imported UI runtime. The references serve design reasoning; third-party code, screenshots and artwork are not included.

The resource study used both requirement-led search (supported Markdown and image mechanisms) and opportunity-led browsing (effective front-page demonstrations and editorial sequencing). The candidates are documented for their inspected roles; the choice follows this project's audience and publishing environment.

## Design representation

**Hierarchy.** Product name and positioning first, then the adapted theme-aware visual identity, quick installation and a first-use prompt. Deeper paragraphs explain the resource-led method and how it works across actual media. A reference table shows the reusable foundations of this very README. The main operation path, sources and verification appear subsequently. The detailed maintainer workflow stays in a native `<details>` block.

**Typography and spacing.** GitHub owns selectable prose, code and headings at its supported fonts and reading measure. The editorial image uses Georgia serif display and system sans for annotations, consistent across theme variants. Geometry, type size and spacing are editable in the source generator rather than fixed by raster cropping.

**Media.** The process plate shows three linked states: studying a documented source, evaluating the fit with a typography/selection cue, and expressing a published reading surface. Actual product UI screenshots remain available in the linked app example; the README is its own media-specific demonstration.

**Interaction.** Links, copyable code, anchor navigation, horizontal code scrolling and disclosure are GitHub-native. The document owns ordinary vertical scrolling. Light/dark and narrow/wide artwork variants keep their critical relationship legible; essential commands, source decisions and constraints remain native text.

## Editable source and delivery

The visual system uses the four generated assets below and one small Python standard-library script:

- [`tools/readme_art.py`](../../tools/readme_art.py): palette tokens, editorial composition, SVG geometry and output generation.
- `docs/assets/studio-light.svg` and `studio-dark.svg`: wide reading-art variants.
- `docs/assets/studio-compact-light.svg` and `studio-compact-dark.svg`: independent narrow compositions.

Regenerate and check the art:

```bash
python tools/readme_art.py
python tools/readme_art.py --check
```

The original README exercise was completed against v1.4.0. Its artwork and reading structure remain the foundation for subsequent documentation updates. Current installation examples follow the repository's `VERSION`; version-specific release and review records identify the corresponding Skill changes and executed checks.

## Inspection plan and evidence levels

1. **Static contracts:** validate all relative links and image paths, standalone SVG safety and version/install strings. Run package validation, source regression tests and deterministic asset checks.
2. **Local render:** use the existing [Markdown-It/Chromium preview script](../../tools/preview_readme.py) in English/Chinese, light/dark, at 390×844, 768×1024 and 1440×1000. Capture each real viewport and full document, inspect visual hierarchy, art variants, native command selection, disclosure, and document overflow. Code/table overflow may be scoped to their containers.
3. **Published host:** GitHub Actions reopens the exact committed README in GitHub and checks actual images, document width and native controls. Read back this evidence separately from the local approximation.
4. **Judgment:** review the visible first screen, visual scale, content density and reader's first-use path. Manual aesthetic conclusions remain scoped to the inspected frames. A successful render is evidence of the tested artifact, not a comparative test of Agent design quality on every screen-based medium.

### 2026-10-25 local iteration

The source-format and link validator passed. The 126 existing tests passed after preserving the README's documented resource-guide reference. Local Chromium rendered 12 language/theme/viewport combinations with viewports and full-page captures, tested first copyable installation text, disclosure and absence of document-level horizontal overflow. The opening screens at 1440 light, 390 light/dark and 390 Chinese were visually inspected; the lead was shortened so the primary install command enters the narrow first viewport. The wide and compact SVG plates were viewed separately after regenerating the source.

The local renderer uses Markdown-It with a GitHub-like stylesheet. Actual GitHub-hosted visual evidence and exact-source checks are recorded by the repository workflow for the published commit; this document distinguishes those observations from source-level and local-render checks.

## Transferable lesson for general screen-based design

The same professional cycle can improve a document by choosing the **host-native document foundation** rather than a component library. Product UI may instead inherit a page shell or component system; a diagram inherits a representation technique; a presentation inherits an editorial sequence and editable source. Their medium-specific completion conditions differ. This README supplies observed evidence for a GitHub publication, while the other media require their own task-based implementation and inspection.

## Visual inspection method in the current reading path

The visual-observation introduction follows the resource method and precedes the
content and runtime sections. It explains how real viewing informs the choices
already introduced, using frames, changing interactions and connected journeys as
its three scopes. The primary install command, editorial artwork and first-use
prompt keep their existing positions. Detailed capture conditions and temporal
qualities live in the linked [visual guide](../VISUAL-INSPECTION.md).

Review each language in the existing theme/viewport matrix. Inspect paragraph
measure, section rhythm and links at their actual size, including lower sections
through document scrolling. The current version's review record owns actual
observations; this section records the design decision and verification scope.

## Product alignment and active exploration in 1.8

The existing foundation section now explains the product's target experience,
named or agent-discovered references, and the two layers of reuse. The observation
section turns relevant visual clues into browsing actions and explains attribution
and evidence sufficiency. Keep the install path, native reading structure and
existing artwork intact. The resource-reuse guide remains a visible next step.

Local review on 2026-10-26 opened all 24 viewport/full-document images across the
declared bilingual/theme/viewport matrix, plus readable crops of the changed
sections. Restoring the resource-guide link required a final recapture and visual
recheck of all 12 affected section crops; the preceding full-image review and the
final localized recheck retain their separate source identities. The
[version review](../REVIEW-v1.8.0.md) records hashes, findings and limits. GitHub
rendering of the published commit has its own CI evidence and visual readback.
