from pathlib import Path
import pandas as pd
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "pbp_derived"
OUT.mkdir(parents=True, exist_ok=True)
TARGETS = {2008: "DET", 2017: "CLE"}
frames = []
for season, team in TARGETS.items():
    path = RAW / f"play_by_play_{season}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run src/download_target_pbp.py first.")
    df = pd.read_csv(path, low_memory=False)
    df = df[df["season"] == season].copy()
    df["target_team"] = team
    # Preserve source rows; analysis filters to plays where the target team possessed
    # the ball or defended. Exclude no-play records from per-play efficiency rates.
    frames.append(df)
pbp = pd.concat(frames, ignore_index=True)
pbp.to_csv(OUT / "raw_target_seasons_pbp.csv", index=False)

# Team offense: plays with the target team in possession. EPA and success rate
# are calculated only where source fields are non-null and play is not a no-play.
offense = pbp[pbp["posteam"].isin(["DET", "CLE"])].copy()
if "no_play" in offense:
    offense = offense[offense["no_play"] != 1]
if "epa" in offense:
    offense["epa_numeric"] = pd.to_numeric(offense["epa"], errors="coerce")
if "success" in offense:
    offense["success_numeric"] = pd.to_numeric(offense["success"], errors="coerce")
agg = []
for (season, team), g in offense.groupby(["season", "posteam"], dropna=False):
    row = {"season": int(season), "team_abbr": team, "offensive_play_rows": len(g)}
    if "epa_numeric" in g:
        row["epa_per_play"] = g["epa_numeric"].mean()
        row["epa_plays_n"] = int(g["epa_numeric"].notna().sum())
    if "success_numeric" in g:
        row["success_rate"] = g["success_numeric"].mean()
        row["success_plays_n"] = int(g["success_numeric"].notna().sum())
    for col in ["pass", "rush", "yards_gained", "air_yards", "yards_after_catch",
                "interception", "fumble_lost", "touchdown", "sack", "qb_hit",
                "third_down_converted", "fourth_down_converted", "game_id", "drive"]:
        if col in g:
            if col in ["game_id", "drive"]:
                row[f"unique_{col}s"] = int(g[col].nunique(dropna=True))
            else:
                vals = pd.to_numeric(g[col], errors="coerce")
                row[f"{col}_sum"] = float(vals.sum(skipna=True))
    agg.append(row)
pd.DataFrame(agg).to_csv(OUT / "offensive_pbp_summary.csv", index=False)

# Team-game rows: score from source game-level final-score columns if present.
game_cols = [c for c in ["game_id", "season", "week", "game_date", "home_team",
                          "away_team", "home_score", "away_score"] if c in pbp]
if {"game_id", "season"}.issubset(game_cols):
    game = pbp[game_cols].drop_duplicates("game_id")
    game = game[(game["home_team"].isin(["DET", "CLE"])) | (game["away_team"].isin(["DET", "CLE"]))]
    game.to_csv(OUT / "target_team_game_metadata.csv", index=False)

print("Built target-season play-by-play tables. Check row counts, missingness, and field definitions before inference.")
