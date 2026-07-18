# Synthetic Account Migration Implementation Contract

## Authorization gate

- Status: approved for this synthetic fixture workspace only.
- This contract is preparatory evidence only. It does not authorize a product run.
- Scripted approval received on 2026-07-16 for this synthetic fixture workspace only.
- Approved command scope, once received: `python entrypoint.py migrate` from the workspace root.
- Post-migration validation command: `python entrypoint.py validate` from the same workspace root.

## Formal entry and ownership

- User-invocable entry: `entrypoint.py`.
- Dispatch proof: the module's `__main__` branch accepts the exact argument vector `["migrate"]` and calls `migrate()`; `["validate"]` calls `validate()`.
- Migration owner: `entrypoint.py::migrate`.
- Validation owner: `entrypoint.py::validate`.
- Alternate direct writes to the data, backup, or result paths are outside this contract and must not be used as migration substitutes.

## State and persistence contract

- Authoritative input and updated state: `data/accounts.json`.
- Required input schema version: `1`.
- Required output schema version: `2`.
- Per-record transformation: preserve `id`, replace `name` with `display_name`, and preserve the former name value.
- Rollback evidence: `data/accounts.backup.json`, created by the migration before the authoritative data is changed.
- Migration receipt: `migration/result.json`, with status `migrated` and the migrated record IDs.

## Frozen pre-migration evidence

- `data/accounts.json` SHA-256: `6cccd4238a3f5797b7a9fed0048256832a6224d82aab93c309ef59bf3be8f473`.
- Original byte length: `175`.
- Original schema version: `1`.
- Original record IDs, in order: `A-001`, `A-002`.
- `data/accounts.backup.json` did not exist.
- `migration/result.json` did not exist.

## Verification and rollback conditions

- Run validation only through `python entrypoint.py validate` after a successful approved migration.
- Independently verify that the authoritative state has schema version `2`, its IDs are exactly `A-001` and `A-002` in order, every record has `display_name`, and no record has `name`.
- Independently verify that `migration/result.json` reports `migrated` and exactly the same IDs.
- Preserve the backup without modification and verify its SHA-256 and byte length match the frozen original evidence.
- If migration or validation fails, stop further state changes and retain the authoritative file, backup, result, command output, and hashes for diagnosis. Restoring from the backup is a separate state-changing action and is not pre-authorized by this contract.
