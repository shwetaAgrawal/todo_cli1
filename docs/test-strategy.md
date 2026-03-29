---
agent-notes:
  ctx: "test pyramid and coverage rules"
  deps: [pyproject.toml, tests/test_cli.py]
  state: active
  last: "codex@2026-03-29"
  key: ["CLI behavior tested through Click runner"]
---
# Test Strategy

**Project:** Todo CLI
**Last reviewed:** 2026-03-29

## Testing Principles

1. Test behavior through the CLI surface first.
2. Keep domain and persistence logic easy to unit test.
3. Every bug gets a regression test before the fix.
4. Preserve a healthy pyramid: unit-heavy, minimal end-to-end.

## Test Pyramid

### Unit Tests

- **Scope:** Due-date parsing, status validation, rendering helpers, store edge cases
- **Coverage target:** 85%+ on business logic
- **Framework:** `pytest`
- **Run command:** `uv run pytest`
- **Speed target:** Full suite under 10 seconds

### Integration Tests

- **Scope:** End-to-end CLI command flow against a temp JSON database
- **Coverage target:** Core CRUD workflow and overdue display
- **Framework:** `pytest` + `click.testing.CliRunner`
- **Run command:** `uv run pytest`
- **Dependencies:** Temporary filesystem only

### End-to-End Tests

- **Scope:** None for MVP
- **Coverage target:** Add only if packaging or shell integration becomes complex
- **Framework:** Not yet selected
- **Run command:** N/A
- **Flaky test policy:** No flaky tests accepted

## What Gets Tested Where

| Area | Unit | Integration | E2E | Notes |
|------|------|-------------|-----|-------|
| Due-date parsing | Yes | Yes | — | Invalid values should fail clearly |
| Status transitions | Yes | Yes | — | Simple fixed statuses for MVP |
| JSON persistence | Yes | Yes | — | Test empty and populated stores |
| CLI commands | — | Yes | — | Primary public interface |
| ANSI overdue rendering | Yes | Yes | — | Verify red highlight for overdue items |

## What Is NOT Tested

| Area | Reason |
|------|--------|
| Shell completion scripts | Not part of MVP |
| Packaging to standalone binaries | Deferred until distribution matters |

## Coverage Gates

| Scope | Metric | Threshold | Enforced by |
|-------|--------|-----------|-------------|
| Overall | Line coverage | 80% | CI + review |
| New code | Behavior coverage | Required | Code review |
| Critical paths | CRUD + list flow | 100% of commands | Tara review |

## Test Data Strategy

- Use temp directories and `TODO_CLI_DB_PATH` for storage isolation.
- Keep fixtures small and explicit.
- No real user data is needed or allowed.
