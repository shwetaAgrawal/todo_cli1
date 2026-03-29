---
agent-notes: { ctx: "implementation tracking for CLI validation", deps: [src/todo_cli/cli.py, tests/test_cli.py], state: active, last: "codex@2026-03-29" }
---

# Implementation: CLI Validation

**Date:** 2026-03-29
**Lead:** codex
**Status:** Complete
**Prior Phase:** None

## Key Decisions

- Chose `click.ClickException` over raw `ValueError` because CLI users need actionable terminal output.
- Chose to validate due-date parsing through a shared helper so add and update commands stay consistent.
- Kept missing-task behavior on the existing command surface because it already matched the desired UX.

## Artifacts Produced

- `src/todo_cli/cli.py`
- `tests/test_cli.py`

## Open Questions

- Whether future validation should distinguish malformed dates from impossible calendar values with different messages.

## Next Phase

- Archived at Sprint 1 boundary after issue `#3` reached `Done`.
