# agent-notes: { ctx: "todo CLI command surface", deps: ["src/todo_cli/models.py", "src/todo_cli/store.py"], state: active, last: "codex@2026-03-29" }
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import click

from todo_cli.models import TASK_STATUSES, Task, parse_due_date
from todo_cli.store import TaskStore


def get_store() -> TaskStore:
    return TaskStore()


def parse_due_date_or_exit(raw_due_date: str) -> date:
    try:
        return parse_due_date(raw_due_date)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


def format_task(task: Task, today: Optional[date] = None) -> str:
    today = today or date.today()
    due_text = task.due_date.isoformat()
    if task.status != "done" and task.due_date < today:
        due_text = click.style(due_text, fg="red")
    return f"{task.id}. [{task.status}] {task.title} (due: {due_text})"


def filter_tasks(
    tasks: list[Task],
    *,
    overdue: bool,
    due_today: bool,
    status: Optional[str],
) -> list[Task]:
    today = date.today()
    filtered = tasks
    if status:
        filtered = [task for task in filtered if task.status == status]
    if overdue:
        filtered = [task for task in filtered if task.status != "done" and task.due_date < today]
    if due_today:
        filtered = [task for task in filtered if task.due_date == today]
    return filtered


@click.group()
def cli() -> None:
    """Manage personal todo items."""


@cli.command()
@click.argument("title")
@click.option("--due", required=True, help="Due date in YYYY-MM-DD format.")
def add(title: str, due: str) -> None:
    """Add a task."""
    store = get_store()
    tasks = store.load()
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, title=title, status="todo", due_date=parse_due_date_or_exit(due))
    tasks.append(task)
    store.save(tasks)
    click.echo(f"Added task {task.id}.")


@cli.command(name="list")
@click.option("--overdue", is_flag=True, help="Show only overdue tasks.")
@click.option("--today", "due_today", is_flag=True, help="Show only tasks due today.")
@click.option(
    "--status", type=click.Choice(TASK_STATUSES), help="Show only tasks with this status."
)
def list_tasks(overdue: bool, due_today: bool, status: Optional[str]) -> None:
    """List tasks."""
    tasks = get_store().load()
    tasks = filter_tasks(tasks, overdue=overdue, due_today=due_today, status=status)
    if not tasks:
        click.echo("No tasks found.")
        return
    for task in sorted(tasks, key=lambda item: (item.due_date, item.id)):
        click.echo(format_task(task), color=True)


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", help="New task title.")
@click.option("--due", help="New due date in YYYY-MM-DD format.")
@click.option("--status", type=click.Choice(TASK_STATUSES), help="New task status.")
def update(task_id: int, title: Optional[str], due: Optional[str], status: Optional[str]) -> None:
    """Update a task."""
    tasks = get_store().load()
    for task in tasks:
        if task.id == task_id:
            if title:
                task.title = title
            if due:
                task.due_date = parse_due_date_or_exit(due)
            if status:
                task.status = status
            get_store().save(tasks)
            click.echo(f"Updated task {task_id}.")
            return
    raise click.ClickException(f"Task {task_id} not found.")


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task."""
    tasks = get_store().load()
    remaining = [task for task in tasks if task.id != task_id]
    if len(remaining) == len(tasks):
        raise click.ClickException(f"Task {task_id} not found.")
    get_store().save(remaining)
    click.echo(f"Deleted task {task_id}.")


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as done."""
    tasks = get_store().load()
    for task in tasks:
        if task.id == task_id:
            task.status = "done"
            get_store().save(tasks)
            click.echo(f"Completed task {task_id}.")
            return
    raise click.ClickException(f"Task {task_id} not found.")


@cli.command(name="export")
@click.argument("destination")
def export_tasks(destination: str) -> None:
    """Export tasks to a backup file."""
    exported = get_store().export_to(Path(destination).expanduser())
    click.echo(f"Exported {exported} task(s).")


@cli.command(name="import")
@click.argument("source")
def import_tasks(source: str) -> None:
    """Import tasks from a backup file."""
    imported = get_store().import_from(Path(source).expanduser())
    click.echo(f"Imported {imported} task(s).")
