from pathlib import Path
import requests
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
SEASONS = [2008, 2017]
BASE = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.csv"
for year in SEASONS:
    url = BASE.format(year=year)
    dest = OUT / f"play_by_play_{year}.csv"
    print(f"Downloading {year}: {url}")
    response = requests.get(url, timeout=90)
    response.raise_for_status()
    dest.write_bytes(response.content)
    # Basic sanity check before accepting a downloaded file.
    sample = pd.read_csv(dest, nrows=5)
    required = {"game_id", "season", "week", "posteam", "defteam"}
    missing = required - set(sample.columns)
    if missing:
        dest.unlink(missing_ok=True)
        raise ValueError(f"{year}: downloaded file missing expected columns {sorted(missing)}")
    print(f"Saved {dest} ({dest.stat().st_size:,} bytes)")
