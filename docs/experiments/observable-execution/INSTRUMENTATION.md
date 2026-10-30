# Correction to media preservation

The original nine runs used the exact recorder preserved in
`inputs/record_design_message.py`. It archived message text and contemporary app
source, but only referenced media by workspace path. The independent audit found
a concrete limitation: T1-k2 message 004's `desktop.png` was later recaptured under
the same name. The current archived pixels match the later neutral background,
while that message's exact source still contains the earlier greener background.

The study therefore retains the original message and source, marks the overwritten
media limitation, and withdraws any claim that this generic image is immutable
evidence of the early pixels. Source differences establish the color repair;
neither a recreated screenshot nor the final image is retroactively inserted into
the original message record. Independent product review inspects frozen final
applications separately.

After the nine runs were frozen, `tools/record_design_message.py` was hardened to
save referenced local media bytes in a separate per-message ZIP with their hashes.
It identifies missing media and declines to read references outside the experiment
workspace. Tests exercise later replacement of the same image path, missing files
and workspace boundaries. This is experiment instrumentation; it adds no installed
Skill field, mandatory design document, lifecycle or approval requirement.

The original nine runs are not re-recorded. Their common input recorder remains
unchanged. The same-SPEC continuation of T2-k2 uses the media-freezing variant,
whose actual source is retained with that continuation. These later capabilities
must not be credited to the original comparison's evidence. The recorder preserves
historical media independently; a generic working-path link may still change, so
historical inspection should use the corresponding frozen media archive. Actual
viewing and human acceptance remain separate facts.
