def process_event(event, store):
    state = store.load()
    state["processed_count"] = state.get("processed_count", 0) + 1
    state["last_event_id"] = event["id"]
    store.save(state)
    return {"accepted": True, "duplicate": False}
