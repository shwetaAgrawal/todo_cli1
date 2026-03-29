---
agent-notes: { ctx: "ADR for Python CLI stack", deps: [CLAUDE.md, pyproject.toml], state: active, last: "codex@2026-03-29" }
---
# ADR-0003: Use Python Click CLI With uv Tooling

## Status

Accepted

## Context

The project needs a fast-to-build personal CLI todo application with local persistence, test coverage, and low setup friction.

## Decision

Use Python 3.9+ with Click for the command-line interface, `uv` for dependency and command management, `pytest` for testing, and Ruff plus pre-commit for code quality checks.

## Consequences

### Positive

- Rapid iteration for a small personal tool
- Mature CLI ergonomics with minimal framework weight
- Straightforward testing for command behavior
- Simple onboarding with one package manager and one lint/format tool

### Negative

- Not as strongly typed or as distributable as a Rust binary
- Packaging as a single native executable would need extra work later

### Neutral

- The project can still evolve to richer terminal UX later without changing the core language choice
