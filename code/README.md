# What's Here

## Python Script: Generate All Derived Datasets

The Python script does the following:

- Loads all raw CSVs under the `weather/raw/YYYY/` folder
- Generates:
  - Monthly summaries
  - Yearly summaries
  - Monthly anomalies
  - Yearly anomalies
  - Charts (PNG)
- Writes outputs into the correct derived/ folders

It uses only the Python standard libraries + `pandas` + `matplotlib`.

---

## PowerShell Script: Generate All Derived Datasets

The powershell version mirrors the Python logic but uses PowerShell + `Import-Csv` + `System.Drawing` for plotting the charts.

### Naming Convention Used for Charts & Anomaly Files

The following princples are used to encourage consistency:

- ISO‑8601 sortable
- Machine‑friendly
- Human‑readable
- Consistent across years

#### Charts

**Monthly charts:**

The following file naming convention is used:

- `temps_YYYY-MM.png`
- `conditions_YYYY-MM.png`
- `precip_YYYY-MM.png`
- `wind_YYYY-MM.png`

**Yearly Charts:**

The following file naming convention is used:

- `temps_YYYY.png`
- `conditions_YYYY.png`
- `precip_YYYY.png`
- `wind_YYYY.png`

#### Anomalies

The following file naming convention is used:

**Monthly Anomalies:** `anomalies_YYYY-MM.csv`

**Yearly Anomalies:** `anomalies_YYYY.csv`

#### Optional Extensions

If more anomaly types are defined at a later date, the following naming convention is suggested:

- `anomalies_temp_YYYY-MM.csv`
- `anomalies_conditions_YYYY-MM.csv`
- `anomalies_precip_YYYY-MM.csv`

Or for Chart file types:

- `temps_trend_YYYY.png`
- `conditions_frequency_YYYY-MM.png`
