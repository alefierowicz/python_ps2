from __future__ import annotations

from typing import Any, ClassVar

from serializable import Serializable

STATUSES = ("pending", "in progress", "done")
STATUS_LABELS = {"pending": "oczekujące", "in progress": "w realizacji", "done": "zrobione"}


class Task(Serializable):
    registry: ClassVar[dict[str, type[Task]]] = {}
    marker: ClassVar[str] = " "

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Task.registry[cls.__name__] = cls

    def __init__(self, title: str, description: str = "", status: str = "pending") -> None:
        self.title = title
        self.description = description
        self.status = status

    def next_status(self) -> None:
        # done zostaje done
        i = STATUSES.index(self.status)
        self.status = STATUSES[min(i + 1, len(STATUSES) - 1)]

    @property
    def due_date(self) -> str | None:
        return None

    def score(self) -> int:
        return 0

    def _details(self) -> list[str]:
        return []

    # serializacja
    def _kwargs(self) -> dict[str, Any]:
        return {"title": self.title, "description": self.description, "status": self.status}

    def to_dict(self) -> dict[str, Any]:
        return {"task_type": type(self).__name__, "kwargs": self._kwargs()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return create_task(data["task_type"], **data["kwargs"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __lt__(self, other: Task) -> bool:
        # status, scoring malejaco, termin (brak na koniec), tytul
        def key(t: Task) -> tuple:
            return (STATUSES.index(t.status), -t.score(), t.due_date is None, t.due_date or "", t.title)
        return key(self) < key(other)

    def __str__(self) -> str:
        info = ", ".join([STATUS_LABELS[self.status], *self._details()])
        return f"[{self.marker}] {self.title} ({info})"


def create_task(task_type: str, **kwargs: Any) -> Task:
    if task_type not in Task.registry:
        raise ValueError(f"Unknown task type: {task_type}")
    return Task.registry[task_type](**kwargs)
