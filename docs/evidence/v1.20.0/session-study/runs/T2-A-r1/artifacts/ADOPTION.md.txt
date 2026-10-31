# Source adoption and design decisions

## Boundary and retained foundation

This package uses the supplied assistant-ui cloud-template composition at revision `ff654d8156680b839774296ef644b57ab1078425`, MIT. The sidebar, header, message measure, user bubble, typography, action bars, composer frame, send/stop hierarchy, menus, dialogs, theme tokens and runtime remain that mature implementation. The original LICENSE and font OFL notices remain in the product. No replacement visual system was constructed.

Final provenance is in `evidence/provenance-complete/source-audit.json`. Of the 35 manifest-listed source files, 32 remain byte-identical. Three are adapted: attachment.aui.tsx, thread.aui.tsx and markdown-text.tsx. The original bytes for all three were reacquired from the exact revision and match the supplied digests; their original files and unified diffs are retained alongside the audit.

## Observed candidates, distinguished from adopted implementation

| Resource | Actual observation | Consequence |
| --- | --- | --- |
| Supplied complete assistant-ui workspace | Baseline desktop and compact composer, seeded reading, streaming/manual-scroll/return/stop episode | Keep the coherent whole. Anonymous 56px file tiles and return-follow/focus behavior warrant a narrow increment. |
| [assistant-ui composer attachments](https://www.assistant-ui.com/elements/composer-attachments) | Rendered live demo with filename-bearing chips in the complete composer; source acquired at the pinned revision | Adopt the actual ComposerAttachmentChip. Its 44px body, 32px icon, 12px filename, 11px metadata, neutral field and persistent remove affordance fit the existing family. |
| [AI Elements attachments](https://elements.ai-sdk.dev/components/attachments) | Rendered inline and list variants; registry source preserved | Compare compact inline badges with larger metadata rows. Inline sacrifices persistent detail and list consumes more vertical room. Neither justifies replacing the source family. |
| [AI Elements conversation](https://elements.ai-sdk.dev/components/conversation) and chatbot example | Rendered complete chatbot with populated answer, suggestion row and composer actions; registry implementation available | Confirms that conversation, compose controls and bottom following should be evaluated together. It remains an independent reference, not copied production code. |
| [HuggingChat](https://huggingface.co/chat/) | Welcome view, then sign-in wall after Start chatting | Public-product research gap. No authenticated composing, streaming or stop behavior was observed or inferred. No code adopted. |

Public screenshots and original request logs are in `evidence/public-verified/`; original web outputs are `evidence/web-001.json` and `web-002.json`. Views were actually opened through view_image, recorded under `evidence/view-public-*.json`. The initial Chromium TLS failure and registry 403 remain preserved. The successful public captures fulfill browser GET requests with the original urllib-fetched bytes, using environment-trusted TLS verification; they do not disable certificate validation or reconstruct the pages. The 359 resource request records include URLs, byte sizes and SHA-256 values. Auth-gated HuggingChat is recorded separately under `evidence/product-reference/`.

## Exact adoption and adaptations

The new `app/src/components/assistant-ui/elements/attachment-chip.tsx` selectively copies ComposerAttachmentChip from `packages/ui/src/components/react/assistant-ui/elements/composer.tsx` at the pinned revision. The fetched original is `evidence/public-verified/aui-composer.tsx`. It retains source surface helpers, radius, spacing, font sizes and icon/removal composition. An optional removeLabel supports Chinese copy; the equivalent source progress percentage helper is local to avoid importing unrelated composer parts.

The existing attachment component composes this chip with the existing Base UI Tooltip. Its filename is an accessible group label and full detail is explicitly described by the tooltip. Focus or tap opens disclosure; blur, outside press or Escape closes it. A focused trigger ignores incidental tooltip close requests, and clicking its nested remove button does not refocus the removed trigger. These are behavior/compatibility adaptations of the mature component, with no replacement popup styling.

Selected files wrap within a maximum 112px scrollable region. The textarea remains native and source-controlled, with a cap of min(12rem,25dvh). The source thread uses its supported bottom turn anchor and autoScroll configuration. Manual scroll-away disables following through the source controller; Return to latest resumes it. No custom forcing scroll loop was added. Markdown smoothing stays on during a run and flushes received buffered text when the run stops. Cancel and removal restore composer focus.

Localized copy is confined to relevant composer/message controls and disclosure. The upstream sidebar and shell retain some English labels. TypeScript 7 compatibility removes obsolete baseUrl, makes the @ path explicit, and adds the standard Vite client declaration. Package dependencies and lockfile are unchanged.

## Design tradeoff

Filename identity consumes space. At 1280×600, a six-line draft with four files is 309px tall versus the baseline's approximately 270px, leaving about 203px between the fixed header and composer. This is an intentional cost for visible identity, not a density improvement. A very long draft stays at 150px input height at this viewport; its scroll height reached 1160px without expanding the composer further. On 390px width, the file region shows roughly two rows with the remaining files reachable by scrolling. None are removed or hidden from the runtime.

## Failed trials and repairs retained

- Baseline return-to-latest did not keep pace with later chunks; Stop lost textarea focus and smoothing continued showing buffered text.
- A dynamic top-to-bottom anchor trial failed because the runtime treats these as initial options. Final configuration uses the supported static bottom mode.
- Initial tooltip assertions exposed missing explicit semantics, then touch exposed incidental dismissal and nested-remove focus bubbling. Commands 013, 018–023 and 028 retain the observations; command 030 confirms the final five touch/focus checks.
- A Chinese edit harness attempted a source action hidden until message hover; command 024 exercises the visible source affordance and passes. Command 023 used an incorrect English input label; command 028 uses the actual label.
- Initial TypeScript checks exposed starter compatibility errors; command 032 passes.
- The two early detail attempts reused the details-final screenshot directory; their independent command stdout retains both exact result sets. The first failing touch image was also preserved in the actual view-image response. Final attempts use distinct directories.

No child agents were used, as required by ALLOCATION.md. Design decisions and final image inspection remained with this package owner.

