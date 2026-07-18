_ASCII_LOWERCASE = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


def normalize_label(value: str) -> str:
    collapsed = " ".join(value.split())
    return collapsed.translate(_ASCII_LOWERCASE)
