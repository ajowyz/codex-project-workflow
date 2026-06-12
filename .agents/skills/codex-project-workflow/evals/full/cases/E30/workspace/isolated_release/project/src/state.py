def record_session(account_id, state):
    state["sessions"].append(account_id)
    return {"accepted": True}
