from datetime import date
from draw_n import get_commit_dates, render_preview


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
    dates = get_commit_dates()
    week1 = [d for d in dates if date(2024, 1, 8) <= d <= date(2024, 1, 12)]
    assert week1 == [date(2024, 1, 9)]


def test_col2_only_wednesday():
    dates = get_commit_dates()
    week2 = [d for d in dates if date(2024, 1, 15) <= d <= date(2024, 1, 19)]
    assert week2 == [date(2024, 1, 17)]


def test_col3_only_thursday():
    dates = get_commit_dates()
    week3 = [d for d in dates if date(2024, 1, 22) <= d <= date(2024, 1, 26)]
    assert week3 == [date(2024, 1, 25)]


def test_preview_has_5_rows():
    lines = render_preview()
    assert len(lines) == 5


def test_preview_row0_shape():
    lines = render_preview()
    assert '█' in lines[0]
    assert '2024-01-01' in lines[0]
    assert '2024-01-29' in lines[0]


def test_preview_col1_dot_except_row1():
    lines = render_preview()
    assert lines[0].count('█') == 2  # only col0 and col4
