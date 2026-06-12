import json
from pathlib import Path


class JsonStateStore:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return {"processed_count": 0}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, state):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
