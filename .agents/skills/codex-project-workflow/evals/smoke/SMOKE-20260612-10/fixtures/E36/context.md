# Production Migration Context

A production billing service uses OpenAI's Assistants API. The team intends to move to the Responses API, and vendor documentation and platform behavior may have changed since the integration was designed.

Analyze these independent read-only questions:

1. Interface and tool-calling compatibility.
2. Data retention, privacy, and state-management implications.
3. Migration sequencing, rollback, and verification.

An incorrect recommendation could interrupt billing operations. The work must use public documentation only; no private source code, customer data, credentials, or internal identifiers may be sent to network tools. No permission has been given to start child agents.
