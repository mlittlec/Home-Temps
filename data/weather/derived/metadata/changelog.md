# Weather Dataset Changelog

This file records all changes to the weather data schema, vocabulary, and processing logic.

---

## v1.0 — Initial Release (2026-09-10)

### Added
- Created initial folder structure for raw and derived datasets.
- Added `schema_v1.json` describing:
  - date (ISO-8601)
  - min_temp (°C)
  - max_temp (°C)
  - conditions (semicolon-separated list)
- Added MET-Office-style controlled vocabulary (`vocabulary_conditions.txt`).
- Added initial processing notes (`processing_notes.md`) covering:
  - monthly summaries
  - yearly summaries
  - anomaly detection
  - chart generation
- Added this changelog.

### Notes
- This is the baseline version for all future schema and processing updates.
