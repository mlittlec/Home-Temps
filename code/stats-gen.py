"""
weather_pipeline.py

Generate derived weather datasets from monthly CSV files.

Input:
    weather/raw/YYYY/weather_daily_YYYY-MM.csv

Outputs:
    weather/derived/
        summaries/
        anomalies/
        charts/

Dependencies:
    pandas
    matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Root directory containing raw weather observations.
RAW_ROOT = Path("weather/raw")

# Root directory for all derived datasets.
DERIVED_ROOT = Path("weather/derived")


def load_month(year, month):
    """
    Load a single monthly weather CSV.

    Parameters
    ----------
    year : int
        Year to load.
    month : int
        Month to load.

    Returns
    -------
    pandas.DataFrame
        Monthly weather observations.
    """

    file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"
    return pd.read_csv(file)


def ensure(path):

    """
    Ensure a directory exists.

    Creates the directory and any missing parent
    directories if they do not already exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def generate_monthly_summary(df, year, month):

    """
    Generate summary statistics for a single month.

    Creates:
        derived/summaries/monthly/YYYY/summary_YYYY-MM.csv
    """

    outdir = DERIVED_ROOT / "summaries" / "monthly" / str(year)
    ensure(outdir)

    # Split semicolon-separated condition values into
    # individual observations and determine the three
    # most frequently occurring conditions.
    dominant_conditions = ";".join(
        df["conditions"]
        .str.split(";")
        .explode()
        .value_counts()
        .head(3)
        .index
    )

    summary = {
        "year": year,
        "month": month,
        "avg_min_temp": df["min_temp"].mean(),
        "avg_max_temp": df["max_temp"].mean(),
        "min_of_min_temp": df["min_temp"].min(),
        "max_of_max_temp": df["max_temp"].max(),
        "dominant_conditions": dominant_conditions,
    }

    pd.DataFrame([summary]).to_csv(
        outdir / f"summary_{year}-{month:02d}.csv",
        index=False,
    )


def generate_yearly_summary(year):

    """
    Generate aggregate statistics for an entire year.

    Creates:
        derived/summaries/yearly/summary_YYYY.csv
    """

    outdir = DERIVED_ROOT / "summaries" / "yearly"
    ensure(outdir)

    frames = []

    # Load all available monthly files.
    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"

        if file.exists():
            frames.append(pd.read_csv(file))

    # Skip processing if no data exists.
    if not frames:
        return

    df = pd.concat(frames, ignore_index=True)

    summary = {
        "year": year,
        "avg_min_temp": df["min_temp"].mean(),
        "avg_max_temp": df["max_temp"].mean(),
        "min_of_min_temp": df["min_temp"].min(),
        "max_of_max_temp": df["max_temp"].max(),
    }

    pd.DataFrame([summary]).to_csv(
        outdir / f"summary_{year}.csv",
        index=False,
    )


def generate_monthly_anomalies(df, year, month):

    """
    Detect temperature anomalies within a month.

    An anomaly is currently defined as any daily record
    having an absolute Z-score greater than 2 for either
    minimum or maximum temperature.

    Creates:
        derived/anomalies/YYYY/anomalies_YYYY-MM.csv
    """

    outdir = DERIVED_ROOT / "anomalies" / str(year)
    ensure(outdir)

    # Create a copy to avoid modifying the caller's dataframe.
    df = df.copy()

    # Compute Z-scores.
    df["z_min"] = (
        (df["min_temp"] - df["min_temp"].mean())
        / df["min_temp"].std()
    )

    df["z_max"] = (
        (df["max_temp"] - df["max_temp"].mean())
        / df["max_temp"].std()
    )

    # Flag potential anomalies.
    anomalies = df[
        (df["z_min"].abs() > 2)
        | (df["z_max"].abs() > 2)
    ]

    anomalies.to_csv(
        outdir / f"anomalies_{year}-{month:02d}.csv",
        index=False,
    )


def generate_yearly_anomalies(year):

    """
    Detect temperature anomalies across an entire year.

    Creates:
        derived/anomalies/yearly/anomalies_YYYY.csv
    """

    outdir = DERIVED_ROOT / "anomalies" / "yearly"
    ensure(outdir)

    frames = []

    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"

        if file.exists():
            frames.append(pd.read_csv(file))

    if not frames:
        return

    df = pd.concat(frames, ignore_index=True)

    df["z_min"] = (
        (df["min_temp"] - df["min_temp"].mean())
        / df["min_temp"].std()
    )

    df["z_max"] = (
        (df["max_temp"] - df["max_temp"].mean())
        / df["max_temp"].std()
    )

    anomalies = df[
        (df["z_min"].abs() > 2)
        | (df["z_max"].abs() > 2)
    ]

    anomalies.to_csv(
        outdir / f"anomalies_{year}.csv",
        index=False,
    )


def generate_monthly_charts(df, year, month):

    """
    Generate monthly temperature trend chart.

    Creates:
        derived/charts/YYYY/temps_YYYY-MM.png
    """

    outdir = DERIVED_ROOT / "charts" / str(year)
    ensure(outdir)

    plt.figure(figsize=(10, 4))

    # Plot daily minimum temperatures.
    plt.plot(
        df["date"],
        df["min_temp"],
        label="Min Temp",
    )

    # Plot daily maximum temperatures.
    plt.plot(
        df["date"],
        df["max_temp"],
        label="Max Temp",
    )

    plt.title(f"Temperature Trends {year}-{month:02d}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        outdir / f"temps_{year}-{month:02d}.png"
    )

    plt.close()


def generate_yearly_charts(year):

    """
    Generate yearly temperature trend chart.

    Creates:
        derived/charts/yearly/temps_YYYY.png
    """

    outdir = DERIVED_ROOT / "charts" / "yearly"
    ensure(outdir)

    frames = []

    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"

        if file.exists():
            frames.append(pd.read_csv(file))

    if not frames:
        return

    df = pd.concat(frames, ignore_index=True)

    plt.figure(figsize=(12, 5))

    plt.plot(
        df["date"],
        df["min_temp"],
        label="Min Temp",
    )

    plt.plot(
        df["date"],
        df["max_temp"],
        label="Max Temp",
    )

    plt.title(f"Temperature Trends {year}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        outdir / f"temps_{year}.png"
    )

    plt.close()


def main():
    
    """
    Process all available years found under RAW_ROOT.
    """

    # Iterate through each year directory
    # (e.g. weather/raw/2025, weather/raw/2026).
    for year_dir in RAW_ROOT.iterdir():

        if not year_dir.is_dir():
            continue

        year = int(year_dir.name)

        # Process monthly datasets.
        for month in range(1, 13):

            file = year_dir / f"weather_daily_{year}-{month:02d}.csv"

            if file.exists():

                df = pd.read_csv(file)

                generate_monthly_summary(
                    df,
                    year,
                    month,
                )

                generate_monthly_anomalies(
                    df,
                    year,
                    month,
                )

                generate_monthly_charts(
                    df,
                    year,
                    month,
                )

        # Generate yearly outputs after all
        # monthly files have been processed.
        generate_yearly_summary(year)
        generate_yearly_anomalies(year)
        generate_yearly_charts(year)


if __name__ == "__main__":
    main()
