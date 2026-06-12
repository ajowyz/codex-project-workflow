def format_value(value):
    return str(value)


def format_row(record):
    return f"{record['name']}: {format_value(record['value'])}"
