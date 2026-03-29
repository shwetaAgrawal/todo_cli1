# agent-notes: { ctx: "CLI integration tests", deps: ["src/todo_cli/cli.py"], state: active, last: "codex@2026-03-29" }
from __future__ import annotations

import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from click.testing import CliRunner

from todo_cli.cli import cli


def test_help_shows_core_commands() -> None:
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "add" in result.output
    assert "list" in result.output
    assert "update" in result.output
    assert "delete" in result.output
    assert "complete" in result.output


def test_add_and_list_task(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    add_result = runner.invoke(cli, ["add", "Pay rent", "--due", "2026-04-01"])
    list_result = runner.invoke(cli, ["list"])

    assert add_result.exit_code == 0
    assert "Added task 1." in add_result.output
    assert list_result.exit_code == 0
    assert "[todo] Pay rent" in list_result.output
    assert "2026-04-01" in list_result.output


def test_update_changes_status_and_due_date(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    runner.invoke(cli, ["add", "Plan sprint", "--due", "2026-04-05"])
    result = runner.invoke(
        cli,
        ["update", "1", "--status", "in_progress", "--due", "2026-04-06"],
    )
    listed = runner.invoke(cli, ["list"])

    assert result.exit_code == 0
    assert "Updated task 1." in result.output
    assert "[in_progress] Plan sprint" in listed.output
    assert "2026-04-06" in listed.output


def test_delete_removes_task(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    runner.invoke(cli, ["add", "Book dentist", "--due", "2026-04-07"])
    delete_result = runner.invoke(cli, ["delete", "1"])
    list_result = runner.invoke(cli, ["list"])

    assert delete_result.exit_code == 0
    assert "Deleted task 1." in delete_result.output
    assert list_result.output.strip() == "No tasks found."


def test_list_highlights_overdue_tasks(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    overdue = (date.today() - timedelta(days=1)).isoformat()
    runner = CliRunner()

    runner.invoke(cli, ["add", "Submit taxes", "--due", overdue])
    result = runner.invoke(cli, ["list"], color=True)

    assert result.exit_code == 0
    assert "\033[31m" in result.output


def test_add_rejects_invalid_due_date_with_clear_message(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))

    result = CliRunner().invoke(cli, ["add", "Pay taxes", "--due", "03-31-2026"])

    assert result.exit_code != 0
    assert "Due date must use YYYY-MM-DD." in result.output


def test_complete_missing_task_returns_clear_not_found_message(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))

    result = CliRunner().invoke(cli, ["complete", "42"])

    assert result.exit_code != 0
    assert "Task 42 not found." in result.output


def test_list_overdue_shows_only_overdue_tasks(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()
    overdue = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=2)).isoformat()

    runner.invoke(cli, ["add", "Overdue task", "--due", overdue])
    runner.invoke(cli, ["add", "Future task", "--due", future])
    result = runner.invoke(cli, ["list", "--overdue"], color=True)

    assert result.exit_code == 0
    assert "Overdue task" in result.output
    assert "Future task" not in result.output


def test_list_today_shows_only_tasks_due_today(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    runner.invoke(cli, ["add", "Today task", "--due", today])
    runner.invoke(cli, ["add", "Tomorrow task", "--due", tomorrow])
    result = runner.invoke(cli, ["list", "--today"])

    assert result.exit_code == 0
    assert "Today task" in result.output
    assert "Tomorrow task" not in result.output


def test_list_status_shows_only_matching_status(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    runner.invoke(cli, ["add", "Todo task", "--due", "2026-04-10"])
    runner.invoke(cli, ["add", "Started task", "--due", "2026-04-11"])
    runner.invoke(cli, ["update", "2", "--status", "in_progress"])
    result = runner.invoke(cli, ["list", "--status", "in_progress"])

    assert result.exit_code == 0
    assert "Started task" in result.output
    assert "Todo task" not in result.output


def test_list_status_can_combine_with_overdue_filter(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()
    overdue = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=3)).isoformat()

    runner.invoke(cli, ["add", "Overdue started", "--due", overdue])
    runner.invoke(cli, ["update", "1", "--status", "in_progress"])
    runner.invoke(cli, ["add", "Future started", "--due", future])
    runner.invoke(cli, ["update", "2", "--status", "in_progress"])
    result = runner.invoke(cli, ["list", "--status", "in_progress", "--overdue"], color=True)

    assert result.exit_code == 0
    assert "Overdue started" in result.output
    assert "Future started" not in result.output


def test_installed_console_script_shows_help() -> None:
    script_path = Path(sys.executable).with_name("todo-cli")
    result = subprocess.run(
        [str(script_path), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Manage personal todo items." in result.stdout


def test_export_writes_tasks_to_backup_file(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    backup_path = tmp_path / "backup.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    runner.invoke(cli, ["add", "Back up taxes", "--due", "2026-04-12"])
    result = runner.invoke(cli, ["export", str(backup_path)])

    assert result.exit_code == 0
    assert "Exported 1 task(s)." in result.output
    assert backup_path.exists()
    assert "Back up taxes" in backup_path.read_text(encoding="utf-8")


def test_import_restores_tasks_from_backup_file(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    backup_path = tmp_path / "backup.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    backup_path.write_text(
        '[\n  {"id": 1, "title": "Restore me", "status": "todo", "due_date": "2026-04-14"}\n]',
        encoding="utf-8",
    )
    runner = CliRunner()

    result = runner.invoke(cli, ["import", str(backup_path)])
    listed = runner.invoke(cli, ["list"])

    assert result.exit_code == 0
    assert "Imported 1 task(s)." in result.output
    assert "Restore me" in listed.output


def test_export_then_import_round_trip(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "tasks.json"
    backup_path = tmp_path / "backup.json"
    monkeypatch.setenv("TODO_CLI_DB_PATH", str(db_path))
    runner = CliRunner()

    runner.invoke(cli, ["add", "Round trip", "--due", "2026-04-20"])
    runner.invoke(cli, ["update", "1", "--status", "in_progress"])
    export_result = runner.invoke(cli, ["export", str(backup_path)])
    db_path.unlink()
    import_result = runner.invoke(cli, ["import", str(backup_path)])
    listed = runner.invoke(cli, ["list", "--status", "in_progress"])

    assert export_result.exit_code == 0
    assert import_result.exit_code == 0
    assert "Round trip" in listed.output
