# SMOKE-20260612-07

This candidate-only run reuses the formally valid clean baseline from `SMOKE-20260612-06`.

## Improvements

- All three threads exposed exactly one project workflow skill.
- Each thread used one successful project-root-stable reference command.
- Each thread loaded exactly two H2 sections.
- No heading discovery, recursive skill scan, failed helper call, child agent, or fixture change occurred.
- Median tokens improved by 29.6 percent and median duration improved by 30.2 percent versus the clean baseline.
- E04 retained the expected professional solution comparison.

## Remaining Failure

The candidate is not eligible for activation.

- E06 called missing authorization a single-agent fallback, although it later asked for approval.
- E36 treated missing authorization as fallback, completed the three streams itself, and never requested a decision.

The state transition must be explicit: suitable work without permission remains `proposed`. Only explicit refusal or unavailable agents may select the single-agent fallback.
