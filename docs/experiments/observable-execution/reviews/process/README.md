# Independent process review archive

The complete original [review](review.md) is retained byte-for-byte. It independently examines all nine frozen participant runs; it is distinct from the coordinator's process summary and from independent product operation.

## Original audit records

- [evidence-index.json](evidence-index.json): original outward-message and adjacent-source-change index.
- [integrity-check.json](integrity-check.json): message source hashes, first/final snapshots and received relays.
- [family-identities.json](family-identities.json): equal task inputs and identical T3 product bytes.
- [packaging-check.json](packaging-check.json): T2-s8 evidence members retained across the four-volume split.
- [timing-and-display.json](timing-and-display.json): descriptive message spans and early visible-result references.
- [source-diffs.zip](source-diffs.zip): 35 original and normalized diff files, 126,239 bytes, independently extractable.

These are the five JSON files present at the source directory's top level. The [archive index](archive-index.json) records every retained original file's SHA-256 and actual direct or ZIP-member location. Diff normalization was a reviewer reading aid; the original report states its limits. Both raw and normalized diff bytes are preserved, including empty comparisons.

## Reconstructing extracted source and media

The reviewer used 1192 extracted source/media files already present in the study's canonical run archives. They are not duplicated here. Every extracted member was byte-compared with the original ZIP member; all matched. [reconstruction.json](reconstruction.json) lists each source ZIP, its SHA-256 and the original extraction directory relative to the review workspace. Resolve each `archive` path from the [study root](../../); extracting its `selected_members` into the corresponding `restore_directory` recreates exactly the review copies. An original archive can contain additional generated files that the reviewer did not extract. Extract `source-diffs.zip` into the same workspace to restore the reviewer-authored diff paths.

T2-s8 reconstruction uses only `participant-evidence-01.zip` through `participant-evidence-04.zip`, as declared by its [archive index](../../runs/T2-s8/archive-index.json). The superseded monolithic evidence ZIP was neither read nor changed during this archival work. All original applications, messages and media remain in their existing run archives.

The report's observations, failed checks, overwritten-media limitation, timing caveats and absence of full natural-speed playback remain unchanged. Preserving an archive establishes byte identity; it does not establish human acceptance or a general method-quality advantage.
