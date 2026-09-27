# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- `.zenodo.json` adds the `spark-ai-nlp` Zenodo community, so future releases are archived there.
- ADR-001: the "Engine/HLS aligned to A" bit is set to 1 (both sidecar READMEs now cite oes32-residual); removed the stale "PRs in flight" note.
- CI actions bumped to `actions/checkout@v7` and `actions/setup-python@v7` (Node 24).

## [0.1.1] - 2026-09-26

### Changed
- `CITATION.cff` version bump for the Zenodo archival release (DOI 10.5281/zenodo.22985521; concept DOI 10.5281/zenodo.22985520). Later: DOI badge and `.zenodo.json`.

## [0.1.0] - 2026-09-26

### Added
- ADR-001 (normative max-absolute residual, strict `>` failure rule) with the sidecar drift table, `CLAIM_HYGIENE.md` and `CITATION.cff`.
- The normative reference itself is commit `b77b612` (2026-08-15): deterministic residual over two 32-vectors with contract tests on SYNTHETIC inputs.
