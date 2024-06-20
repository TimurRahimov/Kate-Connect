import datetime
from typing import Optional


def time_iso(time: Optional[datetime.datetime]) -> Optional[str]:
    if time is None:
        return
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_time(time_string: Optional[str]) -> Optional[datetime.datetime]:
    if time_string is None:
        return
    return datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")


def utcnow_iso() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
