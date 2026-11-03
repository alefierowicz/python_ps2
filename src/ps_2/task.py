from __future__ import annotations

from typing import Any, ClassVar

from .serializable import Serializable

STATUSES = ("pending", "in progress", "done")


class Task(Serializable):
    registry: ClassVar[dict[str, type[Task]]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Task.registry[cls.__name__] = cls

    def __init__(self, title: str, description: str = "", status: str = "pending") -> None:
        if status not in STATUSES:
            raise ValueError(f"Invalid status: {status!r} (allowed: {STATUSES})")
        self.title = title
        self.description = description
        self.status = status

    # serializacja
    def _kwargs(self) -> dict[str, Any]:
        return {"title": self.title, "description": self.description, "status": self.status}

    def to_dict(self) -> dict[str, Any]:
        return {"task_type": type(self).__name__, "kwargs": self._kwargs()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return create_task(data["task_type"], **data.get("kwargs", {}))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    __hash__ = None  # type: ignore[assignment]


def create_task(task_type: str, **kwargs: Any) -> Task:
    try:
        cls = Task.registry[task_type]
    except KeyError:
        raise ValueError(f"Unknown task type: {task_type}") from None
    return cls(**kwargs)
