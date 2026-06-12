# Decisions

## ADR-001: Legacy queue

- 治理状态：已替代
- 证据状态：已验证
- 替代关系：replaced-by ADR-003
- 决定内容：Use the legacy queue.
- 原因：Initial delivery choice.

## ADR-002: Legacy retry

- 治理状态：已替代
- 证据状态：已验证
- 替代关系：replaced-by ADR-003
- 决定内容：Use fixed retries.
- 原因：Initial retry policy.

## ADR-003: Unified delivery

- 治理状态：已替代
- 证据状态：已验证
- 替代关系：replaces ADR-001, ADR-002
- 替代关系：replaced-by ADR-004
- 决定内容：Unify queue and retry policy.
- 原因：This decision replaces older policy text; prose is not a relation field.

## ADR-004: Current delivery

- 治理状态：已确认
- 证据状态：独立复核
- 替代关系：replaces ADR-003
- 决定内容：Use the current delivery service.
- 原因：It supports current reliability requirements.

## ADR-005: Metrics

- 治理状态：已确认
- 证据状态：已验证
- 替代关系：无
- 决定内容：Record delivery metrics.
- 原因：Operational visibility.

## ADR-006: Alerting

- 治理状态：已确认
- 证据状态：已自查
- 决定内容：Alert on sustained delivery failure.
- 原因：Limit unnoticed outages.
