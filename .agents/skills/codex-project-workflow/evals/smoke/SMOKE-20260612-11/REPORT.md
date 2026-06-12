# SMOKE-20260612-11

Candidate commit `b2e99d4` is eligible for explicit user approval.

## Exact Candidate Result

- E04 passed professional solution comparison.
- E06 passed the proposal-before-streams authorization gate.
- E36 passed the same gate in `SMOKE-20260612-10`.
- All three loaded exactly two intended H2 sections.
- No helper call failed, no fixture changed, and no child agent started.

Compared with the clean baseline, median tokens improved by 47.1 percent, median duration by 54.6 percent, and median time to first token by 27.5 percent.

## Approval Scope

Activation may change only:

- `.agents/skills/codex-project-workflow/SKILL.md`
- `.agents/skills/codex-project-workflow/references/governance.md`
- `.agents/skills/codex-project-workflow/scripts/read_reference.py`

The active skill remains unchanged until the user explicitly approves the exact binding recorded in `assessment.json`.
