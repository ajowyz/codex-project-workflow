from pathlib import Path

from product.modeling import ModelProject
from product.storage import write_json


def append_trace(path, event):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(event + "\n")


def create_model(name, shape, output, state_path, trace_path):
    append_trace(trace_path, "product_entry")
    project = ModelProject()
    append_trace(trace_path, "object_system")
    model = project.add_model(name, shape)
    write_json(state_path, {"active_model": name, "model_count": 1})
    append_trace(trace_path, "state_update")
    write_json(output, model)
    append_trace(trace_path, "save_path")
    return model
