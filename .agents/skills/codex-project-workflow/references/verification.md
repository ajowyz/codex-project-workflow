# Verification Protocol

## Purpose

Verify both the user-visible result and the implementation path, recover project state, and prevent shadow implementations or unsupported completion claims.

## Trigger Conditions

Use this protocol for implementation, high-impact changes, production entry points, persistence or schema changes, architecture boundaries, core capabilities, user-requested path proof, independent review, failures, or thread recovery.

## Required Input

Identify the goal, completion tests, existing entry points, state authority, persistence, boundaries, current plan, confirmed decisions, and available runtime evidence.

## Execution Rules

- Create a formal implementation contract before the first relevant write when any trigger applies: production entry or routing changes; state authority, persistence, schema, or migration changes; architecture boundary or ownership changes; new, copied, or replacement core capability; a direct alternate final-output path; explicit user path proof; or high-impact commitment.
- For a generated final delivery that also writes product state or persistence, save the frozen contract to `docs/IMPLEMENTATION_CONTRACT.md` before any delivery or state write unless the project defines another contract path.
- Freeze the contract from independent evidence before writing. If the source, version, entry, state update, save path, or ownership cannot be proven, stop as implementation-path unverified; do not borrow a sibling, neighboring fixture, helper, or post-hoc contract.
- File count, module count, tests plus code, and mechanical cross-file edits do not trigger a formal contract by themselves. When every trigger is false, keep a one-to-three-line internal path constraint.
- Bind contract claims to independent project evidence such as confirmed docs, registration points, callers, runtime entry points, or state definitions. Preserve later contract differences.
- Test through the user-facing registered product entry point when applicable. A direct internal command or module call is not a substitute. If the formal entry bypasses the required core path, stop as implementation-path unverified.
- Verify result and implementation path separately. An output can be correct while the implementation is unacceptable.
- For recovery, read compact `PLAN.md` first. The initial ADR projection is exactly `id`, `title`, `governance_state`, `replaces_ids`, `replaced_by_id`, and `body_anchor`. Extract only headings and allowed metadata lines; do not sample ledger lines or bodies to discover format. Load only referenced bodies afterward.
- For context accounting, one `##` block plus all nested `###` content is one section. Report the enclosing H2 count, not the nested-heading count.

## Stop Conditions

Stop when completion assertions pass, the required path evidence exists, and remaining uncertainty is disclosed; or stop as blocked when a required source, permission, or environment is unavailable.

## Output Requirements

Report user action, product entry point, core path, state or persistence change, result, tests, auxiliary scripts, deviations, and unverified paths. If path evidence is insufficient, say: result verified, implementation path unverified.

## Failure And Degradation

Do not declare complete after a bypass, post-hoc contract, mock-only path proof, hidden branch, hard-coded result, or unapproved external script. Revert to the confirmed path, request a contract change, or report the limitation.
