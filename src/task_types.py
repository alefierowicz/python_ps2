from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from task import Task, check_date

PRIORITY_SCORES = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


class RegularTask(Task):
    def __init__(self, title: str, description: str = "", status: str = "pending",
                 deadline: str | None = None) -> None:
        super().__init__(title, description, status)
        self.deadline = None if deadline is None else check_date(deadline)

    def _kwargs(self) -> dict[str, Any]:
        return super()._kwargs() | {"deadline": self.deadline}

    @property
    def due_date(self) -> str | None:
        return self.deadline

    def _details(self) -> list[str]:
        return [f"do {self.deadline}"] if self.deadline else []


class PriorityTask(Task):
    marker = "!"

    def __init__(self, title: str, description: str = "", status: str = "pending",
                 *, priority: str) -> None:
        super().__init__(title, description, status)
        if priority not in PRIORITY_SCORES:
            raise ValueError(f"Invalid priority: {priority!r}")
        self.priority = priority

    def _kwargs(self) -> dict[str, Any]:
        return super()._kwargs() | {"priority": self.priority}

    def score(self) -> int:
        return PRIORITY_SCORES[self.priority]

    def _details(self) -> list[str]:
        return [f"priorytet: {self.priority}"]


class RecurringTask(Task):
    marker = "o"

    def __init__(self, title: str, description: str = "", status: str = "pending",
                 *, start_date: str, interval_days: int) -> None:
        super().__init__(title, description, status)
        if not isinstance(interval_days, int) or interval_days < 1:
            raise ValueError(f"Invalid interval_days: {interval_days!r}")
        self.start_date = check_date(start_date)
        self.interval_days = interval_days

    def _kwargs(self) -> dict[str, Any]:
        return super()._kwargs() | {"start_date": self.start_date, "interval_days": self.interval_days}

    @property
    def due_date(self) -> str | None:
        # koniec cyklu
        end = date.fromisoformat(self.start_date) + timedelta(days=self.interval_days)
        return end.isoformat()

    def on_date(self, today: str) -> None:
        # startuje sam, gdy nadejdzie start_date
        if self.status == "pending" and self.start_date <= today:
            self.status = "in progress"

    def _details(self) -> list[str]:
        return [f"co {self.interval_days} dni"]
