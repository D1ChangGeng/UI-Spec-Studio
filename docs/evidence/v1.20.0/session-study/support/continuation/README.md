# Continuation coordinator helpers

These copies preserve the original snapshot/index/blinding logic and replace only the hardcoded coordinator repository/root with UI_STUDY_REPO and UI_STUDY_ROOT. The frozen registration, primary prompts, participant inputs and candidate runtime remain unchanged. Set PYTHONPATH to the parent support directory for shared archive/replay helpers. These scripts index actual retained evidence; they do not synthesize tool output or participant completion.

Large original files (for example a 48 MB browser trace) are split byte for byte into separately verified ZIP payloads without discarding or rewriting their content. The continuation replay helper reassembles and verifies them against the complete original snapshot. This affects evidence packaging only.

The continuation index also reads original arrays of view_image tool records, retaining each full batch unchanged while linking its actual PNGs. The continuation replay entry point resolves its bundled helpers directly and accepts --snapshot-directory for retained incomplete attempts.
