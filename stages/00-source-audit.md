# Stage 00 — Source integrity and intake audit

Governing inputs: `SOURCE_MANIFEST.md` and every file under `sources/normalized/`.

## Work

- Delegate a read-only completeness and contradiction scan to `source_auditor`.
- Verify source files and checksums; identify named capabilities and supplied cards.
- Build a source authority map and contradiction register.
- Classify missing information as blocking, architecture-affecting but deferrable, or implementation-detail.
- Do not design ARK in this stage.

Output: `outputs/stages/00-source-audit.md`.

Gate: all sources inventoried, missing capability cards explicit, source conflicts visible, and the user asked to provide or disposition any blocking missing source.
