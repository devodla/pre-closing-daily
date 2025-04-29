from datetime import datetime, timedelta, date
from typing import List, Optional, Dict, Set

def calculate_reports(
    closing_business_day: int,
    daily_offset: int,
    reference_date: Optional[str] = None,
    holidays: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Calculates reports (pre_closing, closing, and daily) based on business rules.
    """
    reference = _parse_reference_date(reference_date)
    holidays_set = _prepare_holidays(holidays)

    reports = []

    if _is_business_day(reference, holidays_set):
        if _is_first_business_day(reference, holidays_set):
            reports.append(_create_report(reference, _last_business_day_of_previous_month(reference, holidays_set), "pre_closing"))
        if _is_nth_business_day(reference, closing_business_day, holidays_set):
            reports.append(_create_report(reference, _last_business_day_of_previous_month(reference, holidays_set), "closing"))

    base_for_daily = _subtract_days(reference, daily_offset)
    reports.append(_create_report(reference, base_for_daily, "daily"))

    return reports

# --- Helper functions ---

def _parse_reference_date(reference_date: Optional[str]) -> date:
    return datetime.strptime(reference_date, "%Y-%m-%d").date() if reference_date else date.today()

def _prepare_holidays(holidays: Optional[List[str]]) -> Set[date]:
    return {datetime.strptime(d, "%Y-%m-%d").date() for d in holidays} if holidays else set()

def _is_business_day(d: date, holidays: Set[date]) -> bool:
    return d.weekday() < 5 and d not in holidays

def _first_business_day_of_month(d: date, holidays: Set[date]) -> date:
    first = d.replace(day=1)
    while not _is_business_day(first, holidays):
        first += timedelta(days=1)
    return first

def _is_first_business_day(d: date, holidays: Set[date]) -> bool:
    return d == _first_business_day_of_month(d, holidays)

def _last_business_day_of_previous_month(d: date, holidays: Set[date]) -> date:
    last = d.replace(day=1) - timedelta(days=1)
    while not _is_business_day(last, holidays):
        last -= timedelta(days=1)
    return last

def _is_nth_business_day(d: date, n: int, holidays: Set[date]) -> bool:
    current = _first_business_day_of_month(d, holidays)
    count = 0
    while current <= d:
        if _is_business_day(current, holidays):
            count += 1
        if current == d:
            break
        current += timedelta(days=1)
    return count == n

def _subtract_days(d: date, offset: int) -> date:
    return d - timedelta(days=offset)

def _create_report(reference: date, base: date, report_type: str) -> Dict[str, str]:
    return {
        "reference_date": reference.strftime("%Y-%m-%d"),
        "base_date": base.strftime("%Y-%m-%d"),
        "report_type": report_type
    }

def main():  # pragma: no cover
    print("Hello from utils-days!")
    holidays = ["2025-03-03", "2025-03-04", "2025-04-18", "2025-04-21", "2025-05-01", "2025-06-19"]
    closing_days = 3
    daily_days = 1

    print(calculate_reports(closing_days, daily_days, reference_date="2025-02-28", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-01", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-02", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-03", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-04", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-05", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-06", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-03-07", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-17", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-18", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-19", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-20", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-21", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-22", holidays=holidays))
    
    print(calculate_reports(closing_days, daily_days, reference_date="2025-04-30", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-01", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-02", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-03", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-04", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-05", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-06", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-07", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-08", holidays=holidays))

    print(calculate_reports(closing_days, daily_days, reference_date="2025-05-31", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-06-01", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-06-02", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-06-03", holidays=holidays))
    print(calculate_reports(closing_days, daily_days, reference_date="2025-06-04", holidays=holidays))


if __name__ == "__main__": # pragma: no cover
    main()
