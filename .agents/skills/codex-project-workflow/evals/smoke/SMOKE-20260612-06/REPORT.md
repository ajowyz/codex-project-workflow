# SMOKE-20260612-06

This is the first formally valid clean baseline-versus-candidate desktop run.

## Validity

- Baseline exposed no project workflow skill.
- Candidate exposed exactly one `codex-project-workflow` skill.
- All six effective threads used `gpt-5.5` with medium reasoning effort.
- No fixture file changed.
- The earlier rate-limited E04 candidate attempt remains recorded in `invalid_attempts.json` and is excluded from scoring.

## Behavioral Result

- E04 passed professional option comparison and produced a staged SQLite-to-PostgreSQL/Qdrant decision path.
- E06 passed the proactive multi-agent proposal and explicit approval boundary.
- E36 passed freshness detection, multi-agent suitability assessment, and the no-start-before-approval boundary.

## Efficiency Failure

The candidate is not eligible for activation.

- E04 read ten H2 sections across research and governance, exceeding the standard ceiling of two.
- E06 and E36 invoked the reference helper from the wrong directory, scanned the skill tree to recover, and then loaded complete protocols.
- Candidate total tokens increased from 235290 to 341592 (+45.2%).
- Candidate duration increased from 494850 ms to 568467 ms (+14.9%).

The final answers were directionally correct, but the internal execution path was not. The next candidate must use a project-root-stable helper command, fixed minimal section sets, and no heading discovery or recursive skill inspection.
