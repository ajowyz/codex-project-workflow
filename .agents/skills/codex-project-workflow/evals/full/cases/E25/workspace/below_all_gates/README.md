# Event-count fixture

Reconstruct counts from `events/` and `quality/` using `policy.json`.
If a gate is met, the repository slot for the resulting task is
`evaluation_tasks/retrieval-evaluation.json`. The active retrieval engine and
dependency list are evidence, not candidate write targets.
