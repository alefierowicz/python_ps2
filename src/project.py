from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date
from pathlib import Path

from task import Task

SORT_KEYS = {
    "deadline": lambda t: (t.due_date is None, t.due_date or ""),
    "priority": lambda t: -t.score(),
}


class Project:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks: list[Task] = []
        self.current_date = date.today().isoformat()

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def set_date(self, new_date: str) -> None:
        self.current_date = new_date

    def _find(self, title: str) -> Task:
        return next(t for t in self.tasks if t.title == title)

    def mark_task_in_progress(self, title: str) -> None:
        self._find(title).status = "in progress"

    def mark_task_done(self, title: str) -> None:
        self._find(title).status = "done"

    def get_active_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.status != "done"]

    def get_overdue_tasks(self) -> list[Task]:
        return [t for t in self.get_active_tasks()
                if t.due_date is not None and t.due_date < self.current_date]

    def sort_tasks(self, criterion: str = "deadline") -> None:
        # sort stabilny, remisy zostaja w kolejnosci dodania
        self.tasks.sort(key=SORT_KEYS[criterion])

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    # serializacja
    def to_json(self) -> str:
        data = {"name": self.name, "current_date": self.current_date,
                "tasks": [t.to_dict() for t in self.tasks]}
        return json.dumps(data, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> Project:
        data = json.loads(json_str)
        project = cls(data["name"])
        project.current_date = data["current_date"]
        project.tasks = [Task.from_dict(t) for t in data["tasks"]]
        return project

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> Project:
        return cls.from_json(Path(path).read_text(encoding="utf-8"))
