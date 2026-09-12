# What's Here

## Python Script — Generate All Derived Datasets

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

## PowerShell Script — Generate All Derived Datasets

The powershell version mirrors the Python logic but uses PowerShell + `Import-Csv` + `System.Drawing` for plotting the charts.
