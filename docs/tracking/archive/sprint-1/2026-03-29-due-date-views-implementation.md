---
agent-notes: { ctx: "implementation tracking for due-date views", deps: [src/todo_cli/cli.py, tests/test_cli.py], state: active, last: "codex@2026-03-29" }
---

# Implementation: Due-Date Views

**Date:** 2026-03-29
**Lead:** codex
**Status:** Complete
**Prior Phase:** None

## Key Decisions

- Chose `--overdue` and `--today` as focused list views because they cover the most common due-date checks with minimal command complexity.
- Kept due-date filtering in a helper so status filters can layer on later without duplicating list logic.

## Artifacts Produced

- `src/todo_cli/cli.py`
- `tests/test_cli.py`

## Open Questions

- Whether a future `--upcoming` view should include a configurable date range.

## Next Phase

- Start issue `#5` for status-based filtering.
