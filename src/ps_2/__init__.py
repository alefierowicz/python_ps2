from .project import Project
from .serializable import Serializable
from .task import STATUSES, Task, create_task
# import rejestruje podklasy w Task.registry
from .task_types import Priority, PriorityTask, RecurringTask, RegularTask

__all__ = [
    "Priority", "PriorityTask", "Project", "RecurringTask", "RegularTask",
    "STATUSES", "Serializable", "Task", "create_task",
]


def main() -> None:
    print("Hello from ps-2!")
