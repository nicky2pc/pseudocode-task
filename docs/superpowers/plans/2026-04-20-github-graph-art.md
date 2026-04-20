# GitHub Graph Art — Letter N Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Python script that backfills backdated commits into `cex-cex` to render the letter N on GitHub's contribution graph for January 2024.

**Architecture:** A single script `draw_n.py` with pure functions for date calculation and ASCII preview, followed by git commit creation using subprocess with `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` env vars. Tests cover the date logic only (no subprocess in tests).

**Tech Stack:** Python 3, subprocess, datetime, pytest

---

## File Map

- Create: `draw_n.py` — main script (date logic + commit creation + CLI)
- Create: `tests/test_draw_n.py` — unit tests for date generation

---

### Task 1: Date generation logic

**Files:**
- Create: `draw_n.py`
- Create: `tests/test_draw_n.py`

The N pattern (5 rows × 5 cols, row=weekday offset from Mon, col=week offset):
```
Col:  0  1  2  3  4
Row0: 1  0  0  0  1
Row1: 1  1  0  0  1
Row2: 1  0  1  0  1
Row3: 1  0  0  1  1
Row4: 1  0  0  0  1
```

Jan 1 2024 = Monday. `date(row, col) = Jan 1, 2024 + col*7 + row days`.

- [ ] **Step 1: Write failing tests**

Create `tests/test_draw_n.py`:
```python
from datetime import date
from draw_n import get_commit_dates

def test_returns_sorted_dates():
    dates = get_commit_dates()
    assert dates == sorted(dates)

def test_first_date_is_jan1():
    dates = get_commit_dates()
    assert dates[0] == date(2024, 1, 1)

def test_last_date_is_feb2():
    dates = get_commit_dates()
    assert dates[-1] == date(2024, 2, 2)

def test_total_commit_count():
    # col0=5, col1=1, col2=1, col3=1, col4=5 → 13
    dates = get_commit_dates()
    assert len(dates) == 13

def test_col1_only_tuesday():
    from datetime import date
    dates = get_commit_dates()
    # Col 1 = week of Jan 8. Only Jan 9 (Tuesday) should be present from Jan 8-12
    week1 = [d for d in dates if date(2024,1,8) <= d <= date(2024,1,12)]
    assert week1 == [date(2024, 1, 9)]

def test_col2_only_wednesday():
    from datetime import date
    dates = get_commit_dates()
    week2 = [d for d in dates if date(2024,1,15) <= d <= date(2024,1,19)]
    assert week2 == [date(2024, 1, 17)]

def test_col3_only_thursday():
    from datetime import date
    dates = get_commit_dates()
    week3 = [d for d in dates if date(2024,1,22) <= d <= date(2024,1,26)]
    assert week3 == [date(2024, 1, 25)]
```

- [ ] **Step 2: Run to confirm failure**

```bash
cd /Users/nick/Desktop/Work/Code/hh/cex-cex
python -m pytest tests/test_draw_n.py -v
```
Expected: `ModuleNotFoundError: No module named 'draw_n'`

- [ ] **Step 3: Implement `get_commit_dates` in `draw_n.py`**

Create `draw_n.py`:
```python
from datetime import date, timedelta

N_PATTERN = [
    [1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1],
]

START_DATE = date(2024, 1, 1)  # Monday


def get_commit_dates() -> list[date]:
    dates = []
    for col in range(5):
        for row in range(5):
            if N_PATTERN[row][col]:
                dates.append(START_DATE + timedelta(days=col * 7 + row))
    return sorted(dates)
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
python -m pytest tests/test_draw_n.py -v
```
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add draw_n.py tests/test_draw_n.py
git commit -m "feat: add N pattern date generation with tests"
```

---

### Task 2: ASCII preview

**Files:**
- Modify: `draw_n.py`
- Modify: `tests/test_draw_n.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_draw_n.py`:
```python
from draw_n import render_preview

def test_preview_has_5_rows():
    lines = render_preview()
    assert len(lines) == 5

def test_preview_row0_shape():
    lines = render_preview()
    # Row 0: █ . . . █ with dates
    assert '█' in lines[0]
    assert '2024-01-01' in lines[0]
    assert '2024-01-29' in lines[0]

def test_preview_col1_dot_except_row1():
    lines = render_preview()
    # Row 0, col 1 should be '.'
    assert lines[0].count('█') == 2  # only col0 and col4
```

- [ ] **Step 2: Run to confirm failure**

```bash
python -m pytest tests/test_draw_n.py::test_preview_has_5_rows -v
```
Expected: `ImportError: cannot import name 'render_preview'`

- [ ] **Step 3: Implement `render_preview`**

Add to `draw_n.py` after `get_commit_dates`:
```python
def render_preview() -> list[str]:
    lines = []
    for row in range(5):
        parts = []
        for col in range(5):
            if N_PATTERN[row][col]:
                d = START_DATE + timedelta(days=col * 7 + row)
                parts.append(f"█ {d}")
            else:
                parts.append("·      ")
        lines.append("  ".join(parts))
    return lines
```

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/test_draw_n.py -v
```
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add draw_n.py tests/test_draw_n.py
git commit -m "feat: add ASCII preview renderer"
```

---

### Task 3: Commit creation and CLI

**Files:**
- Modify: `draw_n.py`

- [ ] **Step 1: Add commit creation + main block**

Append to `draw_n.py`:
```python
import subprocess
import os
import sys


def make_backdated_commit(d: date) -> None:
    date_str = d.strftime("%Y-%m-%dT12:00:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "."],
        env=env,
        check=True,
    )


def main() -> None:
    print("\nLetter N preview:\n")
    for line in render_preview():
        print(" ", line)

    dates = get_commit_dates()
    print(f"\n{len(dates)} commits will be created:")
    for d in dates:
        print(f"  {d}")

    answer = input("\nCreate commits? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        sys.exit(0)

    for d in dates:
        make_backdated_commit(d)
        print(f"  committed {d}")

    answer2 = input("\nPush to origin/main? [y/N] ").strip().lower()
    if answer2 != "y":
        print("Commits created locally. Push manually when ready.")
        sys.exit(0)

    subprocess.run(["git", "push"], check=True)
    print("Done! Check your GitHub profile in a few minutes.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Dry-run — run preview only (no commits)**

```bash
python draw_n.py
```
Enter `N` when prompted. Expected output shows the N preview and 13 dates, then exits cleanly with "Aborted."

- [ ] **Step 3: Commit the script**

```bash
git add draw_n.py
git commit -m "feat: add CLI and backdated commit creation"
```

---

### Task 4: Execute

- [ ] **Step 1: Run the script for real**

```bash
python draw_n.py
```
Review the preview and date list carefully, then type `y`.

- [ ] **Step 2: Verify commits locally**

```bash
git log --oneline --after="2023-12-31" --before="2024-02-03" --format="%ad %s" --date=short
```
Expected: 13 lines, dates matching the N pattern exactly.

- [ ] **Step 3: Push**

Script will ask to push, or run manually:
```bash
git push
```

- [ ] **Step 4: Verify on GitHub**

Open `https://github.com/<your-username>/cex-cex` and navigate to the 2024 contribution view. The N should appear in the first 5 weeks of January.
