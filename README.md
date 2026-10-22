# 0–16: Detroit Lions (2008) vs Cleveland Browns (2017)

## Scope
This project compares **only**:
- Detroit Lions, 2008 season
- Cleveland Browns, 2017 season

It intentionally excludes other historical seasons and broad all-time comparisons. The two selected seasons each ended 0–16.

## What is included
- Season-level team and opponent aggregate statistics for both target teams
- All 32 regular-season game-log rows (16 per team)
- Derived game-level margin, total points, absolute margin, cumulative margin, one-score-game flag, and margin bucket
- Situational efficiency aggregates
- Selected player-stat rows available in the source package (explicitly **not** a complete roster panel)
- Direct metric-by-metric comparison
- Target-team league-rank rows for the appropriate year
- Weight-sensitivity rows for the two target teams
- Source manifest, data dictionary, integrity checks, research paper, and presentation
- A narrow, two-season play-by-play acquisition script and play-by-play analysis script

## Core result
Detroit's point differential was -249; Cleveland's was -176. Detroit allowed 517 points, compared with Cleveland's 410. Cleveland gained more yards (4,942 vs 4,292) but committed more turnovers (41 vs 29) and scored fewer points (234 vs 268). This does not produce one universal definition of “worse”: Detroit was worse by point margin and defensive aggregates, while Cleveland was worse in turnovers and converting drives into points.

## Important completeness status
**This is not yet a full play-by-play research dataset.** The package contains validated team-level aggregates and game logs, but the raw nflverse play-by-play CSVs for 2008 and 2017 could not be downloaded in this execution environment because external GitHub downloads failed at DNS resolution. As a result, EPA/play, success rate, explosive plays, full drive-level tables, and complete player-season summaries are not represented as measured results. The scripts are included to build these tables when the raw files are available. No synthetic play-by-play data has been substituted.

## Rebuild play-by-play analysis (requires internet access)
```bash
python -m pip install -r requirements.txt
python src/download_target_pbp.py
python src/build_target_pbp_tables.py
python src/validate_focused_project.py
```

## Data sources
- Pro-Football-Reference 2008 Detroit team page: https://www.pro-football-reference.com/teams/det/2008.htm
- Pro-Football-Reference 2008 Detroit game log: https://www.pro-football-reference.com/teams/det/2008/gamelog/
- Pro-Football-Reference 2017 Cleveland team page: https://www.pro-football-reference.com/teams/cle/2017.htm
- Pro-Football-Reference 2017 Cleveland game log: https://www.pro-football-reference.com/teams/cle/2017/gamelog/
- nflverse data documentation: https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html
- nflverse releases: https://github.com/nflverse/nflverse-data/releases

## File guide
See `docs/data_dictionary.csv`, `docs/source_manifest.csv`, and `docs/completeness_status.csv`.


## Focused v5 additions
This revision adds a research paper in Markdown/DOCX/PDF, a slide deck, static comparison charts, expanded metric comparisons, and a key-contributor player table sourced from the two team-season pages. The project remains strictly limited to the 2008 Lions and 2017 Browns.

## Unfinished play-level analyses
The raw nflverse play-by-play files could not be retrieved in this environment because GitHub DNS resolution failed. Do not treat EPA/play, success rate, explosive-play rates, full drive tables, or play-level special-teams outputs as completed. Use the target-only acquisition scripts when internet access is available.


## Additional v5 artifacts
- `data/player_season_key_contributors.csv`: selected high-impact player rows with field-level source notes; missing values are left blank rather than treated as zero. This is not a full roster panel.
- `visuals/two_team_3d_comparison.png`: 3D descriptive view of the two observations only.
- `visuals/two_team_3d_comparison.html`: interactive 3D view when Plotly is available. Two observations do not support a predictive 3D model.
