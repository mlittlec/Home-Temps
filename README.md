# Home-Temps

This repository holds a record of the maximum & minimum temperatures recorded from the same (shaded) location in our garden over the years.

## CSV File Format Used

The following outlines the CSV File schema used for the data in this repository:

The header row looks like this:

```text
date, min_temp,max_temp,conditions
```

Where:

* `date` - Use an ISO‑8601 format (YYYY-MM-DD).
* `min_temp` - Store as a plain number (no °C or °F).
* `max_temp` - Same format as `min_temp`.
* `conditions` - Free text is fine:  “Sunny”, “Overcast”, “Light rain”, “Fog”, etc.
