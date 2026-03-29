---
agent-notes:
  ctx: "codebase structural overview"
  deps: [pyproject.toml, src/todo_cli/cli.py, src/todo_cli/store.py]
  state: active
  last: "codex@2026-03-29"
  key: ["update when public CLI or storage changes"]
---
# Code Map

Structural overview of the Todo CLI codebase.

## Architecture at a Glance

```text
Click CLI -> service helpers -> JSON store -> local file
     |             |                |
     |             |                -> task serialization
     |             -> due-date + status validation
     -> terminal rendering with overdue highlighting
```

## Dependency Graph

```text
todo_cli.models   -> no internal deps
todo_cli.store    -> todo_cli.models
todo_cli.cli      -> todo_cli.models, todo_cli.store
tests/test_cli.py -> todo_cli.cli
```

## Package / Module Summaries

### `src/todo_cli/models.py` — Task data model

**Purpose:** Defines task records plus parsing and serialization helpers.

| Module | Key Exports | Notes |
|--------|-------------|-------|
| `src/todo_cli/models.py` | `Task`, `TASK_STATUSES`, `parse_due_date()` | Central task shape and validation |

**External deps:** stdlib
**Internal deps:** none

### `src/todo_cli/store.py` — JSON persistence

**Purpose:** Loads and saves tasks from a local JSON file.

| Module | Key Exports | Notes |
|--------|-------------|-------|
| `src/todo_cli/store.py` | `TaskStore`, `default_db_path()` | Supports env override for tests and user config |

**External deps:** stdlib
**Internal deps:** `src/todo_cli/models.py`

### `src/todo_cli/cli.py` — CLI entry point

**Purpose:** Implements user-facing commands for CRUD and status updates.

| Module | Key Exports | Notes |
|--------|-------------|-------|
| `src/todo_cli/cli.py` | `cli` | Click group with add, list, update, delete, complete |

**External deps:** Click
**Internal deps:** `src/todo_cli/models.py`, `src/todo_cli/store.py`

## Test Inventory

| Package | Test Files | Tests | Focus |
|---------|-----------|-------|-------|
| CLI | 1 | 5 | Help text, add/list/update/delete flow, overdue rendering |

## Key Type Flow

`CLI input -> validated title/status/due date -> Task -> JSON record -> rendered terminal rows`

## Config Structure

- `TODO_CLI_DB_PATH`: overrides the default JSON storage location
- Default storage path: `~/.todo-cli/tasks.json`
