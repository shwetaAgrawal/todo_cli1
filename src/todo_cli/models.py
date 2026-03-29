# agent-notes: { ctx: "task model and validation", deps: [], state: active, last: "codex@2026-03-29" }
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, Union

TASK_STATUSES = ("todo", "in_progress", "done")


def parse_due_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Due date must use YYYY-MM-DD.") from exc


@dataclass(slots=True)
class Task:
    id: int
    title: str
    status: str
    due_date: date

    def to_record(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "due_date": self.due_date.isoformat(),
        }

    @classmethod
    def from_record(cls, record: Dict[str, Union[str, int]]) -> "Task":
        return cls(
            id=int(record["id"]),
            title=str(record["title"]),
            status=str(record["status"]),
            due_date=parse_due_date(str(record["due_date"])),
        )
