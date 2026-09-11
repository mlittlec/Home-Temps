# Derived Weather Datasets

This directory contains all **processed**, **aggregated**, and **visualised** outputs generated from the raw daily weather observations stored under `weather/raw/`.

Derived datasets are organised by type (summaries, anomalies, charts, metadata) and follow a predictable, year‑based structure for long‑term maintainability.

## Directory Layout

```text
derived/
  summaries/
    monthly/
      YYYY/
        summary_YYYY-MM.csv
    yearly/
      summary_YYYY.csv

  anomalies/
    YYYY/
      anomalies_YYYY-MM.csv
    yearly/
      anomalies_YYYY.csv

  charts/
    YYYY/
      temps_YYYY-MM.png
      conditions_YYYY-MM.png
    yearly/
      temps_YYYY.png
      conditions_YYYY.png

  metadata/
    schema_v1.json
    vocabulary_conditions.txt
    processing_notes.md
    changelog.md
```

Each subfolder contains a specific class of derived output:

- **summaries/** → monthly and yearly statistical summaries
- **anomalies/** → outlier detection and unusual‑pattern reports
- **charts/** → visualisations (PNG/SVG)
- **metadata/** → schema, vocabulary, processing logic, version history

## Summaries

Summary files provide aggregated statistics for each month and year.

### Monthly summaries

Stored under: `derived/summaries/monthly/YYYY/summary_YYYY-MM.csv`

Typical fields include:

- avg_min_temp
- avg_max_temp
- min_of_min_temp
- max_of_max_temp
- dominant_conditions (top 3)

### Yearly Summaries

Stored under: `derived/summaries/yearly/summary_YYYY.csv`

These aggregate all months in the year.

## Anomalies

Anomaly files highlight unusual or extreme weather behaviour.

Stored under: 

```text
derived/anomalies/YYYY/anomalies_YYYY-MM.csv
derived/anomalies/yearly/anomalies_YYYY.csv
```

Examples of anomalies:

- Temperature outliers (Z‑score based)
- Sudden day‑to‑day changes
- Condition frequency deviations from historical norms

## Charts

Charts provide visual representations of trends and summaries.

Stored under:

```text
derived/charts/YYYY/
derived/charts/yearly/
```

Typical charts:

- Daily temperature line graphs
- Monthly min/max comparisons
- Condition frequency bar charts

Formats: **PNG** or **SVG**

## Metadata

The `metadata/` folder contains documentation and versioning information:

- *schema_v1.json* — formal definition of the raw CSV schema
- *vocabulary_conditions.txt* — controlled MET‑Office‑style condition list
- *processing_notes.md* — rules for generating summaries, anomalies, and charts
- *changelog.md* — version history of schema and processing logic

These files ensure consistent processing across years and allow the dataset to evolve safely.

## Automation Notes

Scripts generating derived datasets should assume:

- Raw data lives under `weather/raw/YYYY/`
- Derived outputs follow the folder structure above
- Schema and vocabulary are defined in `metadata/`
- Multi‑value fields use semicolon separators
- Filenames follow ISO‑8601 patterns (*YYYY-MM*)

This structure is intentionally stable to support:

- batch processing
- incremental updates
- reproducible analysis
- long‑term archival
