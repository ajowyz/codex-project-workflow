# Executor Contract

- Product entry: `session.entry.open_interactive_session`
- Core policy: `session.policy.may_open_session`
- State mutation: `session.state.record_session`
- Required invariant: suspended accounts never reach state mutation.
