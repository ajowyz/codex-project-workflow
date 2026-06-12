from src.labels import normalize_label


def test_normalize_label_trims_outer_space():
    assert normalize_label("  Alpha  ") == "Alpha"
