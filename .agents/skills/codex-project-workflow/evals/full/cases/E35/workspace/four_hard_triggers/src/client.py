def normalize_event(payload):
    event = payload["event"]
    return {"id": event["id"], "status": event["status"]}
