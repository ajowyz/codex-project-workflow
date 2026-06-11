# Verification Protocol

## Purpose

Verify both the user-visible result and the implementation path, recover project state, and prevent shadow implementations or unsupported completion claims.

## Trigger Conditions

Use this protocol for implementation, high-impact changes, production entry points, persistence or schema changes, architecture boundaries, core capabilities, user-requested path proof, independent review, failures, or thread recovery.

## Required Input

Identify the goal, completion tests, existing entry points, state authority, persistence, boundaries, current plan, confirmed decisions, and available runtime evidence.

## Execution Rules

- Create a formal implementation contract before the first relevant write when any trigger applies: production entry or routing changes; state authority, persistence, schema, or migration changes; architecture boundary or ownership changes; new, copied, or replacement core capability; a direct alternate final-output path; explicit user path proof; or high-impact commitment.
- File count, module count, tests plus code, and mechanical cross-file edits do not trigger a formal contract by themselves. When every trigger is false, keep a one-to-three-line internal path constraint.
- Bind contract claims to independent project evidence such as confirmed docs, registration points, callers, runtime entry points, or state definitions. Preserve later contract differences.
- Test through the formal product entry point when applicable. Mock, spy, coverage, or direct module calls may supplement but cannot alone prove the product path.
- Verify result and implementation path separately. An output can be correct while the implementation is unacceptable.
- For recovery, read the compact `PLAN.md` first. Generate only the ADR metadata projection when `DECISIONS.md` exists, then load referenced ADR bodies and PRD sections as needed.

## Stop Conditions

Stop when completion assertions pass, the required path evidence exists, and remaining uncertainty is disclosed; or stop as blocked when a required source, permission, or environment is unavailable.

## Output Requirements

Report user action, product entry point, core path, state or persistence change, result, tests, auxiliary scripts, deviations, and unverified paths. If path evidence is insufficient, say: result verified, implementation path unverified.

## Failure And Degradation

Do not declare complete after a bypass, post-hoc contract, mock-only path proof, hidden branch, hard-coded result, or unapproved external script. Revert to the confirmed path, request a contract change, or report the limitation.
