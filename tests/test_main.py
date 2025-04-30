from src.main import calculate_reports

holidays = ["2025-05-01", "2025-06-19"]
closing_days = 3
daily_days = 1


def test_pre_closing_day():
    result = calculate_reports(closing_days, daily_days, "2025-06-02", holidays)
    report_types = [r["report_type"] for r in result]
    assert "pre_closing" in report_types
    assert "daily" in report_types


def test_closing_day():
    result = calculate_reports(closing_days, daily_days, "2025-06-04", holidays)
    report_types = [r["report_type"] for r in result]
    assert "closing" in report_types
    assert "daily" in report_types


def test_only_daily_weekend():
    result = calculate_reports(
        closing_days, daily_days, "2025-05-04", holidays
    )  # Sunday
    assert len(result) == 1
    assert result[0]["report_type"] == "daily"


def test_only_daily_holiday():
    result = calculate_reports(
        closing_days, daily_days, "2025-05-01", holidays
    )  # Holiday
    assert len(result) == 0


def test_daily_days_more_than_one():
    result = calculate_reports(closing_days, 2, "2025-05-05", holidays)
    daily_report = next(r for r in result if r["report_type"] == "daily")
    assert daily_report["base_date"] == "2025-05-03"


def test_pre_closing_and_daily_on_first_business_day():
    result = calculate_reports(closing_days, daily_days, "2025-05-02", holidays)
    report_types = [r["report_type"] for r in result]
    assert "pre_closing" in report_types
    assert "daily" in report_types


def test_only_daily_when_not_pre_closing_nor_closing():
    # 2025-05-07 -> 4to día útil, no es closing (closing fue el 6)
    result = calculate_reports(closing_days, daily_days, "2025-05-07", holidays)
    report_types = [r["report_type"] for r in result]
    assert report_types == ["daily"]


def test_closing_on_third_business_day_of_month():
    # 2025-05-06 -> 3er día útil -> debe ser closing + daily
    result = calculate_reports(closing_days, daily_days, "2025-05-06", holidays)
    report_types = [r["report_type"] for r in result]
    assert "closing" in report_types
    assert "daily" in report_types
