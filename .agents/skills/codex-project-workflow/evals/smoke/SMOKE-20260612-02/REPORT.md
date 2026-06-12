# SMOKE-20260612-02

This run used project worktrees from the same base commit and produced complete raw rollout evidence for E04, E06, and E36.

It is not a formal activation result. The candidate worktree exposed two discoverable skills named `codex-project-workflow`: the intended active candidate and the historical evaluation artifact at `SMOKE-20260612-01/candidate_skill/SKILL.md`. The baseline disabled the complete skill tree and had no duplicate.

Diagnostic findings:

- E04 kept professional quality but used 79,975 tokens versus 36,909 for baseline and observed 4,283 reference-tool output characters across 8 H2 sections.
- E06 named the three streams and some costs, but did not provide the complete approved proposal fields.
- E36 still selected single-agent execution without first presenting the user decision.
- No fixture file changed and no child agent started.

The duplicate artifact was later renamed to `SKILL.candidate.md` and protected by an automated single-discoverable-skill test.
