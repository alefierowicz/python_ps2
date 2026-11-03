from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Any

from .dates import to_iso
from .task import Task


class Priority(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    @property
    def rank(self) -> int:
        return {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[self.value]


class RegularTask(Task):
    def __init__(self, title: str, description: str = "", status: str = "pending",
                 deadline: str | date | None = None) -> None:
        super().__init__(title, description, status)
        self.deadline = to_iso(deadline)

    def _kwargs(self) -> dict[str, Any]:
        return super()._kwargs() | {"deadline": self.deadline}


class PriorityTask(Task):
    def __init__(self, title: str, description: str = "", status: str = "pending",
                 priority: str = "MEDIUM") -> None:
        super().__init__(title, description, status)
        self.priority = Priority(priority.upper())

    def _kwargs(self) -> dict[str, Any]:
        # czysty str, nie enum
        return super()._kwargs() | {"priority": str(self.priority)}


class RecurringTask(Task):
    def __init__(self, title: str, description: str = "", status: str = "pending",
                 start_date: str | date | None = None, interval_days: int = 7) -> None:
        super().__init__(title, description, status)
        if not isinstance(interval_days, int) or interval_days < 1:
            raise ValueError(f"interval_days must be a positive int, got {interval_days!r}")
        self.start_date = to_iso(start_date or date.today())
        self.interval_days = interval_days

    def _kwargs(self) -> dict[str, Any]:
        return super()._kwargs() | {"start_date": self.start_date, "interval_days": self.interval_days}
