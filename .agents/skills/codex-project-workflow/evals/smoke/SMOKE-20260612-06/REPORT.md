# SMOKE-20260612-06

This is the first probe based on the cleaned `65f3ff2` evaluation baseline.

The candidate branch exposed exactly one `codex-project-workflow` entry in the desktop thread's initial skill list, proving that renaming evaluation candidates to `SKILL.candidate.md` removed the duplicate-skill contamination.

The E04 probe ended before any assistant response because the desktop premium rate-limit record reported `has_credits=false` and `balance=0`. No behavior result is claimed.

Resume this run when desktop capacity is available. Create the remaining baseline/candidate threads from:

- baseline: `codex/eval-smoke-clean-baseline` at `4b47e0d`
- candidate: `codex/eval-smoke-clean-candidate` at `0d66a1f`
