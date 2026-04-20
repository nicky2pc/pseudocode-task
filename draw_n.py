from datetime import date, timedelta

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
