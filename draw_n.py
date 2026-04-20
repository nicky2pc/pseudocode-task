from datetime import date, timedelta
import os
import subprocess
import sys

N_PATTERN = [
    [1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1],
]

START_DATE = date(2024, 1, 1)  # Monday


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


def get_commit_dates() -> list[date]:
    dates = []
    for col in range(5):
        for row in range(5):
            if N_PATTERN[row][col]:
                dates.append(START_DATE + timedelta(days=col * 7 + row))
    return sorted(dates)


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
