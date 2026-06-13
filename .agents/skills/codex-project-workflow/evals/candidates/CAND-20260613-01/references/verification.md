# Verification Protocol

## Purpose

Verify both the user-visible result and the implementation path, recover project state, and prevent shadow implementations or unsupported completion claims.

## Trigger Conditions

Use this protocol for implementation, high-impact changes, production entry points, persistence or schema changes, architecture boundaries, core capabilities, user-requested path proof, independent review, failures, or thread recovery.

## Required Input

Identify the goal, completion tests, existing entry points, state authority, persistence, boundaries, current plan, confirmed decisions, and available runtime evidence.

## Execution Rules

- Before relevant writes, freeze a contract record for production routing; state authority, persistence, schema, or migration; architecture or ownership; new/replacement core capability; alternate final output; explicit path proof; or high impact. It is evidence, not automatically a project file.
- Persist it only when implementation changes routing, state/persistence/schema/migration, architecture/ownership, core capability, or an alternate output; a generated delivery writes product state; or the user/project requires a durable artifact. Path-proof-only and process-risk triggers stay in the execution record.
- Identify the user-invocable CLI, UI, API, or registration entry before freezing. Bind claims to independent docs, registrations, callers, entries, or state definitions. If entry, state, save path, or ownership is unproven, stop as implementation-path unverified; never borrow neighboring, helper, shadow, or post-hoc evidence.
- File/module count, tests plus code, and mechanical cross-file edits do not trigger a contract. If every trigger is false, keep a one-to-three-line path constraint.
- Map requested behavior to its existing responsibility owner. Change each relevant owner; do not duplicate owner logic in callers, entries, tests, helpers, or output paths. For bounded work inspect only the target, owners/callers, and adjacent tests, not unrelated governance or history.
- Trace the existing user entry. Generate/export/save requests do not authorize repairing entry wiring or core code. If the entry bypasses the core path, stop before contract persistence, delivery, state, or product-code writes.
- Verify result and implementation path separately. An output can be correct while the implementation is unacceptable.
- For recovery, read compact `PLAN.md` first. The initial ADR projection is exactly `id`, `title`, `governance_state`, `replaces_ids`, `replaced_by_id`, and `body_anchor`. Extract only headings and allowed metadata lines; do not sample ledger lines or bodies to discover format. Load only referenced bodies afterward.
- For context accounting, one `##` block plus all nested `###` content is one section. Report the enclosing H2 count, not the nested-heading count.

## Stop Conditions

Stop when completion assertions pass, the required path evidence exists, and remaining uncertainty is disclosed; or stop as blocked when a required source, permission, or environment is unavailable.

## Output Requirements

Report user action, product entry point, core path, state or persistence change, result, tests, auxiliary scripts, deviations, and unverified paths. If path evidence is insufficient, say: result verified, implementation path unverified.

## Failure And Degradation

Do not declare complete after a bypass, post-hoc contract, mock-only path proof, hidden branch, hard-coded result, or unapproved external script. Revert to the confirmed path, request a contract change, or report the limitation.
