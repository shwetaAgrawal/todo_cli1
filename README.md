---
agent-notes: { ctx: "project overview and local usage", deps: [pyproject.toml, src/todo_cli/cli.py], state: active, last: "codex@2026-03-29" }
---
# Todo CLI

Personal Python CLI for managing todo items with simple statuses and due dates.

## Features

- Create tasks with a title and due date
- List tasks with status and overdue highlighting
- Update task title, status, or due date
- Delete tasks
- Mark tasks as complete
- Export tasks to a backup file
- Import tasks from a backup file
- Store tasks locally in JSON

## Stack

- Python 3.9+
- Click for the CLI
- `uv` for dependency management and execution
- `pytest` for tests
- Ruff + pre-commit for linting and formatting

## Setup

```bash
uv sync
```

## Usage

```bash
uv run todo-cli --help
uv run todo-cli add "Pay rent" --due 2026-04-01
uv run todo-cli list
uv run todo-cli update 1 --status in_progress
uv run todo-cli complete 1
uv run todo-cli delete 1
uv run todo-cli export /tmp/tasks-backup.json
uv run todo-cli import /tmp/tasks-backup.json
```

Use `TODO_CLI_DB_PATH` to override the local JSON storage path.

## Command Cookbook

Set a dedicated local task file:

```bash
export TODO_CLI_DB_PATH="$HOME/.todo-cli/tasks.json"
```

Create a few tasks:

```bash
uv run todo-cli add "Pay rent" --due 2026-04-01
uv run todo-cli add "Book dentist" --due 2026-04-03
uv run todo-cli add "Submit taxes" --due 2026-03-31
```

Review all tasks:

```bash
uv run todo-cli list
```

Focus on a specific work state:

```bash
uv run todo-cli list --status todo
uv run todo-cli list --status in_progress
uv run todo-cli list --status done
```

Check time-sensitive tasks:

```bash
uv run todo-cli list --today
uv run todo-cli list --overdue
```

Update task details while work is in flight:

```bash
uv run todo-cli update 2 --title "Book dentist appointment" --status in_progress
uv run todo-cli update 2 --due 2026-04-05
```

Finish and clean up tasks:

```bash
uv run todo-cli complete 2
uv run todo-cli delete 3
```

Use a temporary file for experiments or tests:

```bash
TODO_CLI_DB_PATH=/tmp/todo-cli-demo.json uv run todo-cli list
```

Back up and restore your task file:

```bash
uv run todo-cli export "$HOME/todo-backup.json"
uv run todo-cli import "$HOME/todo-backup.json"
```

## Tests

```bash
uv run pytest
```

## Development

```bash
uv run ruff check .
uv run ruff format --check .
pre-commit run --all-files
```
