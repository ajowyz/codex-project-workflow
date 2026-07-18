def normalize_event(payload):
    event = payload["data"]["event"]
    return {"id": event["id"], "status": event["status"]}
