# Implementation Contract: Synthetic Account Migration

## Authorization gate

- Treat the migration as a high-impact state change.
- Do not run the product entry until explicit scripted approval is received for the exact migration command below.
- Approval for migration does not authorize unrelated commands, code changes, or alternate entry paths.

## Formal product entry and ownership

- Working directory: this workspace root.
- Authorized migration entry: `python entrypoint.py migrate`.
- Authorized validation entry after migration: `python entrypoint.py validate`.
- `entrypoint.py` is both the user-invocable CLI and the existing owner of migration and validation behavior. No helper, shadow script, direct data edit, or alternate output path is acceptable.
- Pre-migration `entrypoint.py` SHA-256: `2687510D6E4E4BAE4166FC095F80B75FE8C95A8C7EAC926B92B4581DF2441FD3`.

## Frozen pre-migration state

- Authoritative state: `data/accounts.json`.
- Expected schema version: `1`.
- Expected record IDs in order: `A-001`, `A-002`.
- Pre-migration `data/accounts.json` SHA-256: `6CCCD4238A3F5797B7A9FED0048256832A6224D82AAB93C309EF59BF3BE8F473`.
- `data/accounts.backup.json` and `migration/result.json` must not exist before the approved run.

## Required state transition

- Create `data/accounts.backup.json` as an exact byte-for-byte copy of the frozen schema-version-1 source.
- Change `data/accounts.json` from schema version `1` to `2`.
- Preserve every record ID and its order.
- Replace each record's `name` field with `display_name`, preserving the value.
- Write `migration/result.json` with migration status and the migrated record IDs.

## Rollback and evidence

- The backup must hash to `6CCCD4238A3F5797B7A9FED0048256832A6224D82AAB93C309EF59BF3BE8F473` after migration.
- Preserve the backup after validation as rollback evidence; do not overwrite or delete it.
- A rollback, if later authorized, consists of restoring the authoritative file from that backup. This contract does not authorize rollback execution.

## Verification and stop conditions

- After the approved migration exits successfully, run `python entrypoint.py validate` from the same workspace root.
- Separately inspect the authoritative data, backup, and result artifacts to verify schema, field replacement, IDs, value preservation, paths, and backup hash.
- Stop without invoking the product if the frozen source hash, schema version, IDs, entrypoint hash, or absence of pre-existing backup/result artifacts has changed before approval or execution.
- Report product-entry validation separately from artifact and rollback-evidence verification.
