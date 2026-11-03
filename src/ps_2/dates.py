from __future__ import annotations

from datetime import date


def to_iso(value: str | date | None) -> str | None:
    # walidacja i format yyyy-mm-dd
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    return date.fromisoformat(value).isoformat()
