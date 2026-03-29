---
agent-notes: { ctx: "implementation tracking for console-script fix", deps: [pyproject.toml, scripts/todo-cli, tests/test_cli.py], state: active, last: "codex@2026-03-29" }
---

# Implementation: Console Script Fix

**Date:** 2026-03-29
**Lead:** codex
**Status:** Complete
**Prior Phase:** None

## Key Decisions

- Chose an installed bootstrap script over a generated console entry point because the local editable install path was intermittently failing to expose `src/todo_cli`.
- Kept the bootstrap script searching upward for `src/todo_cli` so local repo runs work while still allowing normal package imports when available.
- Added a subprocess regression test for the installed `todo-cli --help` path because pytest's `pythonpath=src` masked the original packaging failure.

## Artifacts Produced

- `pyproject.toml`
- `scripts/todo-cli`
- `tests/test_cli.py`

## Open Questions

- Whether a later packaging cleanup should revisit the editable install behavior once the underlying `uv` path handling is better understood.

## Next Phase

- Review and close issue `#6`.
