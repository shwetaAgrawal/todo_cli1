---
agent-notes: { ctx: "implementation tracking for backup commands", deps: [src/todo_cli/cli.py, src/todo_cli/store.py, tests/test_cli.py, README.md], state: active, last: "codex@2026-03-29" }
---

# Implementation: Backup Commands

**Date:** 2026-03-29
**Lead:** codex
**Status:** Complete
**Prior Phase:** None

## Key Decisions

- Chose `export <path>` and `import <path>` commands using the existing JSON task schema to keep backup files simple and round-trip safe.
- Kept serialization logic in `TaskStore` so backup behavior and the main data file stay in sync.
- Verified round-trip behavior through the real `uv run todo-cli ...` command path to ensure the feature works outside test helpers.

## Artifacts Produced

- `src/todo_cli/cli.py`
- `src/todo_cli/store.py`
- `tests/test_cli.py`
- `README.md`

## Open Questions

- Whether a future import mode should merge tasks instead of replacing the current store.

## Next Phase

- Close issue `#2` and archive Sprint 2 tracking artifacts at sprint boundary.
