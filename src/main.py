from datetime import datetime, timedelta
from typing import List, Optional, Dict

def calculate_reports(
    closing_days: int,
    daily_days: int,
    reference_date: Optional[str] = None,
    holidays: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Calculates reports (pre_closing, closing, and daily) based on business rules.
    """
    reference = _parse_reference_date(reference_date)
    holidays_set = _prepare_holidays(holidays)

    results = []

    if _is_business_day(reference, holidays_set):
        if _is_first_business_day_of_month(reference, holidays_set):
            results.append(_create_report(reference, _last_business_day_of_previous_month(reference, holidays_set), "pre_closing"))
        elif _is_closing_day(reference, closing_days, holidays_set):
            results.append(_create_report(reference, _last_business_day_of_previous_month(reference, holidays_set), "closing"))

    # Always generate daily report
    daily_base_date = _subtract_days(reference, daily_days)
    results.append(_create_report(reference, daily_base_date, "daily"))

    return results

# --- Helper functions ---

def _parse_reference_date(reference_date: Optional[str]) -> datetime.date:
    return datetime.strptime(reference_date, "%Y-%m-%d").date() if reference_date else datetime.now().date()

def _prepare_holidays(holidays: Optional[List[str]]) -> set:
    if not holidays:
        return set()
    return {datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in holidays}

def _is_business_day(date: datetime.date, holidays: set) -> bool:
    return date.weekday() < 5 and date not in holidays

def _first_business_day_of_month(date: datetime.date, holidays: set) -> datetime.date:
    first_day = date.replace(day=1)
    while not _is_business_day(first_day, holidays):
        first_day += timedelta(days=1)
    return first_day

def _is_first_business_day_of_month(date: datetime.date, holidays: set) -> bool:
    return date == _first_business_day_of_month(date, holidays)

def _last_business_day_of_previous_month(date: datetime.date, holidays: set) -> datetime.date:
    first_day_of_month = date.replace(day=1)
    last_day_previous_month = first_day_of_month - timedelta(days=1)
    while not _is_business_day(last_day_previous_month, holidays):
        last_day_previous_month -= timedelta(days=1)
    return last_day_previous_month

def _subtract_days(date: datetime.date, days: int) -> datetime.date:
    """
    Subtract calendar days (not business days).
    """
    return date - timedelta(days=days)

def _is_closing_day(reference: datetime.date, closing_days: int, holidays: set) -> bool:
    """
    Check if the reference date is the N-th business day of the current month.
    """
    first_business_day = _first_business_day_of_month(reference, holidays)

    business_day_count = 0
    current_date = first_business_day

    while current_date <= reference:
        if _is_business_day(current_date, holidays):
            business_day_count += 1
        if current_date == reference:
            break
        current_date += timedelta(days=1)

    return business_day_count == closing_days

def _create_report(reference_date: datetime.date, base_date: datetime.date, report_type: str) -> Dict[str, str]:
    return {
        "reference_date": reference_date.strftime("%Y-%m-%d"),
        "base_date": base_date.strftime("%Y-%m-%d"),
        "report_type": report_type
    }

def main():
    print("Hello from utils-days!")
    holidays = ["2025-05-01", "2025-06-19"]
    closing_days = 2
    daily_days = 1

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


if __name__ == "__main__":
    main()
