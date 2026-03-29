# agent-notes: { ctx: "JSON persistence for tasks", deps: ["src/todo_cli/models.py"], state: active, last: "codex@2026-03-29" }
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from todo_cli.models import Task


def default_db_path() -> Path:
    override = os.environ.get("TODO_CLI_DB_PATH")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".todo-cli" / "tasks.json"


class TaskStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path or default_db_path()

    def _decode_tasks(self, payload: str) -> list[Task]:
        data = json.loads(payload)
        return [Task.from_record(item) for item in data]

    def _encode_tasks(self, tasks: list[Task]) -> str:
        payload = [task.to_record() for task in tasks]
        return json.dumps(payload, indent=2)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        return self._decode_tasks(self.path.read_text(encoding="utf-8"))

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self._encode_tasks(tasks), encoding="utf-8")

    def export_to(self, destination: Path) -> int:
        tasks = self.load()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(self._encode_tasks(tasks), encoding="utf-8")
        return len(tasks)

    def import_from(self, source: Path) -> int:
        tasks = self._decode_tasks(source.read_text(encoding="utf-8"))
        self.save(tasks)
        return len(tasks)
