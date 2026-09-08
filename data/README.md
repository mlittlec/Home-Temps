# Weather Data Archive

This repository contains structured daily weather observations recorded in CSV format. The layout is designed for long‑term storage, easy manual navigation, and simple automation across multiple years.

## Directory Structure

 ```text
 weather/
  2025/
    weather_daily_2025-01.csv
    weather_daily_2025-02.csv
    ...
  2026/
    weather_daily_2026-01.csv
    weather_daily_2026-02.csv
    ...
 ```

## Why This Structure?

 * Each year is isolated for clarity and scalability.
 * Monthly files keep datasets small and fast to load.
 * Filenames follow ISO‑8601 ordering, making them sortable and script‑friendly.

## File naming convention

Daily weather logs are stored in **monthly CSV files** using the following pattern:

```text
weather_daily_YYYY-MM.csv
```

Examples:

* `weather_daily_2026-07.csv`
* `weather_daily_2026-12.csv`

This naming scheme ensures:

* Natural chronological sorting
* Easy globbing in scripts (weather_daily_2026-*.csv)
* Compatibility across platforms and tools

## CSV Schema

Each CSV file contains daily records with the following fields:

```text
date,min_temp,max_temp,conditions
```

### Field Definitions

* *date* — ISO‑8601 format (YYYY-MM-DD)
* min_temp — minimum temperature (°C), numeric
* max_temp — maximum temperature (°C), numeric
* conditions — one or more weather condition terms

If multiple condition terms are present, they are stored as a semicolon‑separated list inside quotes:

```text
"Rain;Windy;Low visibility"
```

## Weather Conditions Vocabulary

To ensure consistency, the conditions field uses a MET‑Office‑style vocabulary. Terms include:

### Sky & Visibility

* Clear
* Sunny
* Partly cloudy
* Cloudy
* Overcast
* Mist
* Fog
* Freezing fog
* Haze

### Rain & Moisture

* Drizzle
* Light rain
* Heavy rain
* Showers
* Thundery showers
* Thunderstorm

### Snow & Ice

* Sleet
* Snow
* Light snow
* Heavy snow
* Blizzard
* Ice

### Wind

* Breezy
* Windy
* Gales
* Severe gales

### Other

* Humid
* Dry

Multiple terms may be combined when appropriate (e.g., "Light rain;Breezy").

## Usage notes

* All temperatures are recorded in degrees Celsius.
* All files are plain CSV with UTF‑8 encoding.
* Data is intended for long‑term analysis, automation, and visualisation.
* Additional fields (e.g., humidity, wind speed, precipitation) may be added in future versions.

## Automation

Scripts can safely assume:

* Year directories follow YYYY/
* Monthly files follow weather_daily_YYYY-MM.csv
* CSV schema is stable and consistent across years

This makes it easy to build:

* Annual summaries
* Monthly averages
* Trend analysis
* Visual dashboards
