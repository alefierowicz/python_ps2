from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Any

from .dates import to_iso
from .serializable import Serializable
from .task import Task


class Project(Serializable):
    def __init__(self, name: str, tasks: list[Task] | None = None,
                 current_date: str | None = None) -> None:
        self.name = name
        self.tasks: list[Task] = []
        self.current_date = date.today().isoformat()
        if current_date is not None:
            self.set_date(current_date)
        for task in tasks or []:
            self.add_task(task)

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError(f"expected Task, got {type(task).__name__}")
        self.tasks.append(task)

    def set_date(self, new_date: str) -> None:
        self.current_date = to_iso(new_date)

    def _find(self, title: str) -> Task:
        for task in self.tasks:
            if task.title == title:
                return task
        raise KeyError(f"Task not found: {title}")

    def mark_task_in_progress(self, title: str) -> None:
        self._find(title).status = "in progress"

    def mark_task_done(self, title: str) -> None:
        self._find(title).status = "done"

    def get_active_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.status != "done"]

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    def __len__(self) -> int:
        return len(self.tasks)

    def __repr__(self) -> str:
        return f"Project({self.name!r}, {len(self)} tasks, date={self.current_date})"

    # serializacja
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "current_date": self.current_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(data["name"], tasks, data.get("current_date"))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> Project:
        return cls.from_dict(json.loads(json_str))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> Project:
        return cls.from_json(Path(path).read_text(encoding="utf-8"))
