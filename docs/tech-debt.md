---
agent-notes:
  ctx: "technical debt register across sprints"
  deps: [CLAUDE.md]
  state: active
  last: "codex@2026-03-29"
  key: ["Grace tracks, Pat prioritizes against features"]
---
# Technical Debt Register

**Project:** Todo CLI
**Last reviewed:** 2026-03-29

## Active Debt

No active technical debt is currently tracked.

## Resolved Debt

| ID | Description | Incurred | Resolved | How it was fixed |
|----|-------------|----------|----------|-----------------|
| TD-001 | Installed `todo-cli` command failed with `ModuleNotFoundError` in local `uv run` flows | Sprint 2 | Sprint 2 | Reworked the installed command bootstrap and added subprocess regression coverage |

## Debt Categories

| Category | Count | Trend |
|----------|-------|-------|
| Missing tests | 0 | Stable |
| Hardcoded values | 0 | Stable |
| Missing error handling | 0 | Stable |
| Copy-paste duplication | 0 | Stable |
| Outdated dependencies | 0 | Stable |
| Missing docs | 0 | Stable |
| Performance | 0 | Stable |
| Security | 0 | Stable |
| Accessibility | 0 | Stable |

## Review Cadence

- Sprint boundary: review for new debt and prioritize any carry-forward work
- Every 3 sprints: full debt review and re-estimation
