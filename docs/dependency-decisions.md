---
agent-notes:
  ctx: "dependency rationale and license notes"
  deps: [docs/sbom.md, pyproject.toml]
  state: active
  last: "codex@2026-03-29"
---
# Dependency Decisions

## Top-Level Dependencies

### Click

- **Package:** `click`
- **Version:** `>=8.1,<9`
- **License:** BSD-3-Clause
- **Why we're using it:** Stable Python CLI library with strong command and option ergonomics.
- **Alternatives considered:** `typer` was considered, but Click keeps the stack smaller and lines up with the scaffold workflow defaults.
- **Added:** 2026-03-29 by codex

### Pytest

- **Package:** `pytest`
- **Version:** `>=8.0,<9`
- **License:** MIT
- **Why we're using it:** Fast feedback loop and strong CLI testing support through `CliRunner`.
- **Alternatives considered:** `unittest` was possible, but `pytest` keeps tests shorter and clearer.
- **Added:** 2026-03-29 by codex

### Ruff

- **Package:** `ruff`
- **Version:** `>=0.11,<0.12`
- **License:** MIT
- **Why we're using it:** One tool for linting and formatting keeps the project lightweight.
- **Alternatives considered:** Separate `black` + `flake8` setup was rejected to reduce tool sprawl.
- **Added:** 2026-03-29 by codex

### Pre-commit

- **Package:** `pre-commit`
- **Version:** `>=4.0,<5`
- **License:** MIT
- **Why we're using it:** Ensures formatting and lint checks run consistently before commits.
- **Alternatives considered:** CI-only enforcement was rejected because it slows feedback.
- **Added:** 2026-03-29 by codex

## Transitive Dependencies

Transitive dependency inventory will be filled after the first lockfile or SBOM pass.

## License Flags

No flagged transitive licenses yet.
