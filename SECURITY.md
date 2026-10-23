# Security policy

The current 1.x release line receives security fixes. Report vulnerabilities
through the repository's private vulnerability-reporting channel when available,
or contact the maintainer through their GitHub profile to arrange a private
report. Public issues are appropriate for non-sensitive packaging defects.

Include affected version, reproduction steps, impact and the smallest sanitized
example. Keep credentials, private project content and exploitable secret values
in a private channel.

The distributed skill contains Markdown and optional standard-library Python
helpers. Installing it supplies instructions; the host controls execution and
permissions. Review third-party dependencies and external material under that
host's security model. Helpers operate on an explicitly selected local project.

The checker validates records and evidence paths. It does not authenticate user
approval, inspect image contents or certify product security. Evidence files and
approval records remain the operator's responsibility. Release assets contain
reviewed source files and a content inventory; SHA-256 checksums detect byte
changes, while GitHub provenance identifies the publishing source.
