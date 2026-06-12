from src.formatting import format_row


def render_report(records, include_zero=False):
    visible = [record for record in records if record["value"] != 0]
    return "\n".join(format_row(record) for record in visible)
