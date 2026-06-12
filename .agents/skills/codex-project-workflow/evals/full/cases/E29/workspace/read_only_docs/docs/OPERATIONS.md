# Operations

Queue failure recovery is manual. There is no documented reconciliation step
for records written by the API while workers are unavailable.

Database schema changes are deployed independently by the API and worker teams.
