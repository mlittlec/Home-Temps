import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

RAW_ROOT = Path("weather/raw")
DERIVED_ROOT = Path("weather/derived")

def load_month(year, month):
    file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"
    return pd.read_csv(file)

def ensure(path):
    path.mkdir(parents=True, exist_ok=True)

def generate_monthly_summary(df, year, month):
    outdir = DERIVED_ROOT / "summaries" / "monthly" / str(year)
    ensure(outdir)

    summary = {
        "year": year,
        "month": month,
        "avg_min_temp": df["min_temp"].mean(),
        "avg_max_temp": df["max_temp"].mean(),
        "min_of_min_temp": df["min_temp"].min(),
        "max_of_max_temp": df["max_temp"].max(),
        "dominant_conditions": ";".join(
            df["conditions"].str.split(";").explode().value_counts().head(3).index
        )
    }

    pd.DataFrame([summary]).to_csv(
        outdir / f"summary_{year}-{month:02d}.csv", index=False
    )

def generate_yearly_summary(year):
    outdir = DERIVED_ROOT / "summaries" / "yearly"
    ensure(outdir)

    frames = []
    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"
        if file.exists():
            frames.append(pd.read_csv(file))

    df = pd.concat(frames)
    summary = {
        "year": year,
        "avg_min_temp": df["min_temp"].mean(),
        "avg_max_temp": df["max_temp"].mean(),
        "min_of_min_temp": df["min_temp"].min(),
        "max_of_max_temp": df["max_temp"].max(),
    }

    pd.DataFrame([summary]).to_csv(
        outdir / f"summary_{year}.csv", index=False
    )

def generate_monthly_anomalies(df, year, month):
    outdir = DERIVED_ROOT / "anomalies" / str(year)
    ensure(outdir)

    df["z_min"] = (df["min_temp"] - df["min_temp"].mean()) / df["min_temp"].std()
    df["z_max"] = (df["max_temp"] - df["max_temp"].mean()) / df["max_temp"].std()

    anomalies = df[(df["z_min"].abs() > 2) | (df["z_max"].abs() > 2)]
    anomalies.to_csv(outdir / f"anomalies_{year}-{month:02d}.csv", index=False)

def generate_yearly_anomalies(year):
    outdir = DERIVED_ROOT / "anomalies" / "yearly"
    ensure(outdir)

    frames = []
    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"
        if file.exists():
            frames.append(pd.read_csv(file))

    df = pd.concat(frames)
    df["z_min"] = (df["min_temp"] - df["min_temp"].mean()) / df["min_temp"].std()
    df["z_max"] = (df["max_temp"] - df["max_temp"].mean()) / df["max_temp"].std()

    anomalies = df[(df["z_min"].abs() > 2) | (df["z_max"].abs() > 2)]
    anomalies.to_csv(outdir / f"anomalies_{year}.csv", index=False)

def generate_monthly_charts(df, year, month):
    outdir = DERIVED_ROOT / "charts" / str(year)
    ensure(outdir)

    plt.figure(figsize=(10, 4))
    plt.plot(df["date"], df["min_temp"], label="Min Temp")
    plt.plot(df["date"], df["max_temp"], label="Max Temp")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / f"temps_{year}-{month:02d}.png")
    plt.close()

def generate_yearly_charts(year):
    outdir = DERIVED_ROOT / "charts" / "yearly"
    ensure(outdir)

    frames = []
    for month in range(1, 13):
        file = RAW_ROOT / str(year) / f"weather_daily_{year}-{month:02d}.csv"
        if file.exists():
            frames.append(pd.read_csv(file))

    df = pd.concat(frames)

    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df["min_temp"], label="Min Temp")
    plt.plot(df["date"], df["max_temp"], label="Max Temp")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / f"temps_{year}.png")
    plt.close()

def main():
    for year_dir in RAW_ROOT.iterdir():
        if not year_dir.is_dir():
            continue

        year = int(year_dir.name)

        for month in range(1, 13):
            file = year_dir / f"weather_daily_{year}-{month:02d}.csv"
            if file.exists():
                df = pd.read_csv(file)
                generate_monthly_summary(df, year, month)
                generate_monthly_anomalies(df, year, month)
                generate_monthly_charts(df, year, month)

        generate_yearly_summary(year)
        generate_yearly_anomalies(year)
        generate_yearly_charts(year)

if __name__ == "__main__":
    main()
