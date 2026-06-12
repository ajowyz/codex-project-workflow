from session.policy import may_open_session
from session.state import record_session


def open_interactive_session(account_id, state):
    if not may_open_session(account_id, state):
        return {"accepted": False}
    return record_session(account_id, state)
