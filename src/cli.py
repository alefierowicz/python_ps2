from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project import SORT_KEYS, Project
from task import Task, create_task
from task_types import PRIORITY_SCORES

RED, GREEN, DIM, RESET = "\033[31m", "\033[32m", "\033[2m", "\033[0m"
TASK_FIELDS = ("description", "deadline", "priority", "start_date", "interval_days")


def paint(text: str, color: str) -> str:
    return f"{color}{text}{RESET}" if color and sys.stdout.isatty() else text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="menedzer zadan")
    parser.add_argument("-f", "--file", type=Path, default=Path("project.json"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="nowy projekt").add_argument("name")

    add = sub.add_parser("add", help="dodaj zadanie")
    add.add_argument("type", choices=sorted(Task.registry))
    add.add_argument("title")
    add.add_argument("--description")
    add.add_argument("--deadline")
    add.add_argument("--priority", choices=list(PRIORITY_SCORES))
    add.add_argument("--start-date")
    add.add_argument("--interval-days", type=int)

    sub.add_parser("start", help="oznacz jako w realizacji").add_argument("title")
    sub.add_parser("done", help="oznacz jako zrobione").add_argument("title")
    sub.add_parser("date", help="ustaw biezaca date").add_argument("date")

    ls = sub.add_parser("list", help="pokaz zadania")
    ls.add_argument("--sort", choices=list(SORT_KEYS))
    only = ls.add_mutually_exclusive_group()
    only.add_argument("--active", action="store_true")
    only.add_argument("--overdue", action="store_true")
    return parser


def show(project: Project, args: argparse.Namespace) -> None:
    if args.sort:
        project.sort_tasks(args.sort)
    overdue = project.get_overdue_tasks()
    if args.overdue:
        tasks = overdue
    elif args.active:
        tasks = project.get_active_tasks()
    else:
        tasks = list(project)

    print(paint(f"{project.name} (dzis: {project.current_date})", DIM))
    for task in tasks:
        color = GREEN if task.status == "done" else RED if task in overdue else ""
        print(paint(str(task), color))


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == "init":
            if args.file.exists():
                parser.error(f"{args.file} juz istnieje")
            project = Project(args.name)
        else:
            project = Project.load(args.file)

        match args.cmd:
            case "add":
                kwargs = {k: getattr(args, k) for k in TASK_FIELDS if getattr(args, k) is not None}
                project.add_task(create_task(args.type, title=args.title, **kwargs))
            case "start":
                project.mark_task_in_progress(args.title)
            case "done":
                project.mark_task_done(args.title)
            case "date":
                project.set_date(args.date)
            case "list":
                show(project, args)
                return
        project.save(args.file)
    except FileNotFoundError:
        parser.error(f"brak {args.file}, zacznij od: todo init NAZWA")
    except StopIteration:
        parser.error(f"brak zadania: {args.title}")
    except (TypeError, ValueError) as e:
        # np. brak --priority dla priority task
        parser.error(str(e))


if __name__ == "__main__":
    main()
