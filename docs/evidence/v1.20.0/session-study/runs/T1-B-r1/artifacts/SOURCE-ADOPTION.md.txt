# Actual source adoption

## Foundation identity

Tabler 1.7.1, MIT, exact tag commit `07f60c07da13d8ff957a370434b7ef5c86f5ab94`. The original compiled settings page is independently identified by SHA-256 `ed80162e38d7667bfe020b5d16d228c4adc64f301233cfbeeeae6f606697a06e`; its public deployment commit is unknown. SOURCE-MANIFEST.json remains unchanged and preserves the package digest and preparation provenance. The original license remains at app/LICENSE.

## What actually carries the product

| Responsibility | Adopted source and location | Retained / adapted relationship |
| --- | --- | --- |
| Settings page, navigation and surfaces | sources/official-settings-snapshot.html; sources/shared/layouts/SettingsLayout.astro; app/index.html | Existing settings navigation, 3/9 grid, container, card body/footer, border, typography and document scroll retained. |
| Field family, validation and hints | Local 1.7.1 CSS; exact tagged docs/content/ui/forms/validation.mdx retained in evidence/research; app/index.html | Native form-control, form-label, form-hint, is-invalid and invalid-feedback. Added semantic form, required labels, names, descriptions and error associations. Store facts drive the presentation. |
| Save feedback and recovery | sources/shared/ui/Alert.astro; exact tagged alert docs; local CSS | Default alert tint/border, source-supported text-body utility, native button loading state. Footer composition keeps result and retry adjacent. No original alert or spinner drawing. |
| Header fixture controls | Exact PageHeader.astro source, current official page-header documentation | Native row/col/col-auto/ms-auto/btn-list action composition; existing theme and language buttons relocated. |
| Profile identity and long input | Existing avatar family and grid | Source avatar-lg variant; full-width name and col-md-7/col-md-5 supporting fields. No new font, image or decorative asset. |
| Notification and privacy controls | Existing Check.astro switch composition | Native large switch, on/off labels and source focus/checked states; bilingual factual copy and descriptions. |
| Real behavior | Existing settings-store.js, unchanged | UI adapter owns draft comparison, locale, focus and feedback. The store remains the authority for schema, localStorage, validation, delay and failures. |

Only app/index.html and app/settings-controller.js changed in the product. No minified distribution file changed. No dependency was added, and no new lockfile was needed. Existing scripts and package manifest remain runnable. Product changes are summarized by evidence/final-product.diff and the final hashes in evidence/final-source-integrity.json.

## Primary references used

- [Tabler repository at the adopted commit](https://github.com/tabler/tabler/tree/07f60c07da13d8ff957a370434b7ef5c86f5ab94)
- [Official settings demo](https://preview.tabler.io/settings.html)
- [Alert documentation](https://docs.tabler.io/ui/components/alert)
- [Page header documentation](https://docs.tabler.io/ui/layout/page-headers)
- [Tagged validation documentation](https://github.com/tabler/tabler/blob/07f60c07da13d8ff957a370434b7ef5c86f5ab94/docs/content/ui/forms/validation.mdx)
- [Bootstrap field feedback association](https://getbootstrap.com/docs/5.3/forms/validation/)

The primary designer's actual web open/find responses are in evidence/primary-source-open.json and evidence/primary-source-find.json. Current forms guidance is retained in evidence/commands/001-web-search and 002-web-forms. The main source specimens were personally viewed; these are clearly labeled local exact-source renders, not public demo screenshots. The child’s public screenshot-export limitation is preserved in evidence/research/RESEARCH.md.

## Compared, not adopted

Minor alerts, filled important alerts, toast behavior and native browser validation prompts were considered. The primary designer selected field-local feedback plus a persistent footer alert: it answers both correction and operation outcome without introducing an overlay. A browser prompt must not replace the authoritative store rules. Toast source inspection establishes a candidate contract only; no toast runtime is part of this product.

The outer specimen layout in evidence/research is a research composition and was not copied into the product. Additional source snapshots retain their MIT lineage and remain reference material. Future maintenance owns the project adapter; upstream updates must recheck mixed-script text, focus, save sequencing and narrow scrolling.
