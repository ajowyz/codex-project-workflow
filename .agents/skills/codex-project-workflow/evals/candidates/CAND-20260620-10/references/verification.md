# Verification Protocol

## Purpose

Verify both the user-visible result and the implementation path, recover project state, and prevent shadow implementations or unsupported completion claims.

## Trigger Conditions

Use this protocol for implementation, high-impact changes, production entry points, persistence or schema changes, architecture boundaries, core capabilities, user-requested path proof, independent review, failures, or thread recovery.

## Required Input

Identify the goal, completion tests, existing entry points, state authority, persistence, boundaries, current plan, confirmed decisions, and available runtime evidence.

## Execution Rules

- Before relevant writes, freeze an evidence-bound contract in the execution trace for routing, state/schema/migration, architecture/ownership, core capability, alternate output, path proof, or high impact. A contract is not a project file by default.
- If a generated delivery invokes a product that writes state or persistence, create `docs/IMPLEMENTATION_CONTRACT.md` before the first product invocation, even when product code is unchanged. Otherwise path-proof, process-risk, and code-only owner-change contracts stay non-file unless the user or project requires a file.
- Identify the user-invocable CLI, UI, API, or registration entry before freezing. Bind claims to independent docs, registrations, callers, entries, or state definitions. If entry, state, save path, or ownership is unproven, stop as implementation-path unverified; never borrow neighboring, helper, shadow, or post-hoc evidence.
- File/module count, tests plus code, and mechanical cross-file edits do not trigger a contract. If every trigger is false, keep a one-to-three-line path constraint.
- Map requested behavior to its existing responsibility owner. Change each relevant owner; do not duplicate owner logic in callers, entries, tests, helpers, or output paths. For bounded work inspect only the target, owners/callers, and adjacent tests.
- Trace the existing user entry. Generate/export/save requests do not authorize repairing entry wiring or core code. If the entry bypasses the core path, stop before contract, delivery, state, or product-code writes.
- Verify result and implementation path separately. Correct output does not prove acceptable implementation.
- For recovery, read compact `PLAN.md` first. The initial ADR projection is exactly `id`, `title`, `governance_state`, `replaces_ids`, `replaced_by_id`, and `body_anchor`. Extract only headings and allowed metadata lines; load referenced bodies afterward.
- One `##` block plus nested `###` content is one context section.

## Stop Conditions

Stop when completion assertions pass, the required path evidence exists, and remaining uncertainty is disclosed; or stop as blocked when a required source, permission, or environment is unavailable.

## Output Requirements

Report user action, product entry, core path, state/persistence change, result, tests, auxiliary scripts, deviations, and unverified paths. If evidence is insufficient, say: result verified, implementation path unverified.

## Failure And Degradation

Do not declare complete after a bypass, post-hoc contract, mock-only proof, hidden branch, hard-coded result, or unapproved external script. Revert to the confirmed path, request a contract change, or report the limitation.
