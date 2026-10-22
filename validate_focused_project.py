from pathlib import Path
import pandas as pd, json
ROOT = Path(__file__).resolve().parents[1]
checks = []
def check(name, passed, detail):
    checks.append({"check": name, "passed": bool(passed), "detail": str(detail)})
games = pd.read_csv(ROOT / "data" / "team_game_logs.csv")
check("target_game_log_count", len(games)==32, f"rows={len(games)} expected=32")
counts = games.groupby(["season","team_abbr"]).size().to_dict()
check("16_games_each", counts.get((2008,"DET"))==16 and counts.get((2017,"CLE"))==16, counts)
summary = pd.read_csv(ROOT / "data" / "team_season_summary.csv")
for season, abbr, pf, pa, pdiff in [(2008,"DET",268,517,-249),(2017,"CLE",234,410,-176)]:
    rows=summary[(summary.season==season)&(summary.team_abbr==abbr)]
    check(f"{season}_{abbr}_core_totals", len(rows)==1 and int(rows.iloc[0]["points_for"])==pf and int(rows.iloc[0]["points_against"])==pa and int(rows.iloc[0]["point_differential"])==pdiff,
          f"rows={len(rows)} expected PF/PA/PD={pf}/{pa}/{pdiff}")
for season,abbr,pf,pa in [(2008,"DET",268,517),(2017,"CLE",234,410)]:
    g=games[(games.season==season)&(games.team_abbr==abbr)]
    check(f"{season}_{abbr}_game_log_sums", int(g.points_for.sum())==pf and int(g.points_against.sum())==pa,
          f"PF/PA sums={g.points_for.sum()}/{g.points_against.sum()}")
pbp_summary = ROOT / "data" / "pbp_derived" / "offensive_pbp_summary.csv"
check("pbp_output_present", pbp_summary.exists(), "Present only after source download and PBP build")
if pbp_summary.exists():
    d=pd.read_csv(pbp_summary)
    check("pbp_two_targets_only", set(zip(d.season,d.team_abbr)).issubset({(2008,"DET"),(2017,"CLE")}), list(zip(d.season,d.team_abbr)))
out=pd.DataFrame(checks)
out.to_csv(ROOT/"docs"/"validation_checks.csv",index=False)
(ROOT/"docs"/"validation_report.json").write_text(json.dumps({"checks":checks,"all_passed":all(c["passed"] for c in checks)},indent=2))
print(out.to_string(index=False))
