# SMOKE-20260612-01

## Status

Calibration completed. The paired result is not valid for MVP scoring because baseline threads used a projectless desktop environment while candidate threads used a saved project environment. The run remains valid evidence for skill discovery, actual file loading, standalone behavior, test outcomes, and harness design.

## Results

| Case | Baseline | Candidate | Finding |
| --- | --- | --- | --- |
| E01 | 16/16 diagnostic | 16/16 diagnostic | Both changed exactly one line and verified it. Candidate loaded only the 486-character description, not the skill body. |
| E04 | 15/16 diagnostic | 13/16 diagnostic | Both produced a professional five-option comparison. Candidate was 32% slower and loaded all three references: 6,738 characters and 21 H2 sections. |
| E06 | 13/16 diagnostic | 13/16 diagnostic | Both continued safe read-only analysis, but neither proposed multi-agent roles, benefit, cost, risk, or an approval decision. |
| E31 | 16/16 diagnostic | 16/16 diagnostic | Both changed only `src/invoice.py` and passed 2/2 tests. Candidate loaded no skill body, references, or governance documents. Pair remains invalid because the environments differed. |
| E36 | 12/16 diagnostic | 12/16 diagnostic | Both performed current official research and covered all three technical questions. Neither assessed multi-agent suitability. |

No hard failure was proven in this run.

## Pair Metrics

| Case | Candidate / baseline time | Candidate / baseline output length | Candidate / baseline tokens |
| --- | ---: | ---: | ---: |
| E01 | 1.04 | 3.66 | 1.02 |
| E04 | 1.32 | 1.17 | 1.64 |
| E06 | 0.81 | 0.73 | 0.84 |
| E31 | 0.80 | 1.17 | 0.80 |
| E36 | 1.00 | 0.73 | 0.87 |

These ratios are calibration-only. E01 output length is visibly affected by different project versus projectless file-link rules.

## Findings

1. **P1: Multi-agent assessment is not reliably triggered.** E06 and E36 both contained separable read-only streams and high failure cost. The candidate did not present roles, boundaries, benefit, cost, conflict risk, or a single-agent alternative.
2. **P1: Progressive disclosure is not enforced operationally.** E04 loaded every reference file even though only research/options were needed. Its 6,738 reference characters and 21 H2 sections exceeded the standard 2,500-character and two-section budget without an overage record.
3. **P2: The baseline harness is confounded.** Projectless and project threads receive different desktop instructions. The next paired run must use an identical project worktree with only the repository skill disabled.
4. **Positive evidence:** E01 and E31 did not load the skill body or references. The negative-trigger boundary works for these two ordinary tasks.
5. **Positive evidence:** Rollout JSONL is a usable equivalent load trace. It exposes skill metadata, actual skill/reference reads, project-document reads, tools, timing, tokens, output, and file changes.

## Candidate

`candidate_skill/SKILL.md` is an isolated, unapproved candidate. It makes two targeted changes:

- locate headings and read only required H2 blocks, never entire reference files;
- proactively assess multi-agent use when separable streams, independent-review value, or high failure cost are present.

The candidate retains the 486-character description, has a 1,484-character body, and passed full skill validation when overlaid on a temporary copy of the current skill. It is not active and must not replace the repository skill without approval and a corrected paired rerun.
