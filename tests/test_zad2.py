import pytest

from zad2 import Project
from zad2 import Task, RegularTask, PriorityTask, RecurringTask


def test_task_to_dict():
    task1 = RegularTask("Przygotować prezentację", "opis zadania", deadline="2025-10-25")
    task2 = PriorityTask("Złożyć raport", priority="HIGH")
    task3 = RecurringTask("Backup bazy danych", start_date="2025-10-15", interval_days=7)
    assert task1.to_dict()["task_type"] == "RegularTask"
    assert task2.to_dict()["task_type"] == "PriorityTask"
    assert task3.to_dict()["task_type"] == "RecurringTask"


def test_regular_task_to_dict():
    task = RegularTask("Przygotować prezentację", "opis zadania", deadline="2025-10-25")
    task_dict = task.to_dict()
    assert isinstance(task_dict, dict)
    assert "task_type" in task_dict
    assert task_dict["task_type"] == "RegularTask"
    assert "kwargs" in task_dict
    kwargs_dict = task_dict["kwargs"]
    assert "title" in kwargs_dict
    assert "description" in kwargs_dict
    assert "status" in kwargs_dict
    assert "deadline" in kwargs_dict
    assert kwargs_dict["title"] == "Przygotować prezentację"
    assert kwargs_dict["description"] == "opis zadania"
    assert kwargs_dict["status"] == "pending"
    assert kwargs_dict["deadline"] == "2025-10-25"


def test_regular_task_from_dict():
    data = {
        "task_type": "RegularTask",
        "kwargs": {
            "title": "Przygotować prezentację",
            "description": "opis zadania",
            "status": "pending",
            "deadline": "2025-10-25"
        }
    }
    task = Task.from_dict(data)
    assert isinstance(task, RegularTask)
    assert task.title == "Przygotować prezentację"
    assert task.description == "opis zadania"
    assert task.status == "pending"
    assert task.deadline == "2025-10-25"


def test_unknown_task_type_from_dict():
    data = {
        "task_type": "UnknownTask",
        "kwargs": {
            "title": "AAA",
            "description": "BBB",
        }
    }
    with pytest.raises(ValueError, match="Unknown task type: UnknownTask"):
        Task.from_dict(data)


def test_new_task_type():
    class NewTaskType(Task): ...
    data = {
        "task_type": "NewTaskType",
        "kwargs": {
            "title": "AAA",
            "description": "BBB",
        }
    }
    task = Task.from_dict(data)
    assert isinstance(task, NewTaskType)


def test_project_to_json_and_from_json():
    project = Project("Zajecia WI PB")
    project.add_task(RegularTask("Przygotować prezentację", deadline="2025-10-25"))
    project.add_task(PriorityTask("Złożyć raport", priority="HIGH"))
    project.add_task(RecurringTask("Backup bazy danych", start_date="2025-10-15", interval_days=7))
    project.set_date("2025-10-22")
    json_str = project.to_json()
    assert isinstance(json_str, str)
    new_project = Project.from_json(json_str)
    assert project != new_project
    assert project.name == new_project.name
    assert project.current_date == new_project.current_date
    for t1,t2 in zip(project, new_project):
        assert t1 == t2
