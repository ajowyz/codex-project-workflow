_ASCII_LOWERCASE_TABLE = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


def normalize_label(value: str) -> str:
    collapsed = " ".join(value.split())
    return collapsed.translate(_ASCII_LOWERCASE_TABLE)
