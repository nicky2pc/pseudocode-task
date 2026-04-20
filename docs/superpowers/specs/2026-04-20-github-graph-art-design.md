# GitHub Graph Art — Letter N

## Goal

Backfill commits into the `cex-cex` repo to draw the letter **N** on the GitHub contribution graph for January 2024.

## Target Period

January 1 – February 2, 2024. This period is confirmed empty of commits.

## Pixel Pattern

5 rows × 5 columns. Rows map to weekdays Mon–Fri (rows 1–5 in GitHub's Sun-origin grid). Columns map to calendar weeks.

```
Col:  0  1  2  3  4
Row0: █  .  .  .  █   Monday
Row1: █  █  .  .  █   Tuesday
Row2: █  .  █  .  █   Wednesday
Row3: █  .  .  █  █   Thursday
Row4: █  .  .  .  █   Friday
```

## Commit Dates

| Column | Dates |
|--------|-------|
| 0 | Jan 1, 2, 3, 4, 5 |
| 1 | Jan 9 |
| 2 | Jan 17 |
| 3 | Jan 25 |
| 4 | Jan 29, 30, 31, Feb 1, 2 |

## Implementation

Python script (`draw_n.py`) that:
1. Prints ASCII preview of the N with dates
2. Creates backdated empty commits via `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`
3. Prompts user confirmation before `git push`

Each commit message: `"."` (minimal noise in log).
