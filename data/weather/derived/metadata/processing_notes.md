# Processing Notes (v1)

These notes describe how derived datasets (summaries, anomalies, charts) are generated from the raw daily weather CSV files.

---

## Data Sources

All raw data is stored under:

  - `weather/raw/YYYY/weather_daily_YYYY-MM.csv`

Files follow the schema defined in `schema_v1.json`.

---

## Monthly Summaries

Monthly summary files are generated from all records in a given month.

Example output location:

  - `weather/derived/summaries/monthly/YYYY/summary_YYYY-MM.csv`

### Summary fields include:
- month
- avg_min_temp
- avg_max_temp
- min_of_min_temp
- max_of_max_temp
- dominant_conditions (top 3 by frequency)
- total_precip_mm (if available in future schema versions)

---

## Yearly Summaries

Yearly summaries aggregate all months in a given year.

Output location:

  - `weather/derived/summaries/yearly/summary_YYYY.csv`

---

## Anomaly Detection

Anomalies are calculated using:
- Z-score thresholds for temperature outliers
- Sudden day-to-day changes (e.g., >8°C drop)
- Unusual condition frequency compared to historical averages

Output location:

  - `weather/derived/anomalies/YYYY/anomalies_YYYY-MM.csv`
  - `weather/derived/anomalies/yearly/anomalies_YYYY.csv`

---

## Charts

Charts are generated as PNG or SVG files.

Output location:

  - `weather/derived/charts/YYYY/`
  - `weather/derived/charts/yearly/`

Typical charts:
- Daily temperature line graphs
- Monthly min/max comparison
- Condition frequency bar charts

---

## Versioning

Processing logic is versioned independently from the schema.  
Current version: **1.0**

Future versions may add:
- humidity
- wind speed
- precipitation
- sunrise/sunset times
