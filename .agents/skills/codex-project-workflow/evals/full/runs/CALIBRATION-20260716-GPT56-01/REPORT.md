# GPT-5.6-sol calibration baseline

Date: 2026-07-16  
Runtime: Codex App 26.707.12708.0, CLI 0.144.5, `gpt-5.6-sol`, `xhigh`  
Candidate: CAND-20260716-13  
Machine summary: `results-recollected-v2/summary.json`  
Assessment: `assessment.json`

## Result

Overall: **FAIL**. Four of six runs passed; E32 failed as an aggregate case and E35 passed.

- `E32:negative_quick` failed because it loaded the 1485-codepoint skill body and the 2239-codepoint / 2-H2 verification protocol for a simple one-file typo fix. Expected load was `[0, 0]`.
- `E32:standard_cross_file` failed because it loaded governance plus verification at 4723 codepoints / 4 H2. The standard limits are 2500 / 2.
- `E32:full_high_risk_migration`, `E32:hard_trigger_overage`, `E32:nested_h3_counting`, and `E35:four_hard_triggers` passed their declared assertions.

## Evidence boundary

The six tasks started before the project-local discoverable `SKILL.md` was retired, so the run is behavior and failure-baseline evidence, not single-runtime-owner acceptance. P1 owner acceptance is recorded separately in task `019f6a23-82cf-7552-b489-d06f1e72abbf`.

The corrected collection preserves launch-time skill metrics from emitted tool output and recognizes protocol calls in unified-exec backtick templates. The earlier `results/` and `results-recollected/` snapshots are retained as collector-debug evidence; `results-recollected-v2/` is the assessed source.

## Follow-up

CAND-20260716-14 supersedes this candidate. It strengthens the negative activation boundary and limits routine bounded implementation to verification unless a governance trigger exists. It requires a new plugin cache, single-owner acceptance, and all six fresh regressions before activation.
