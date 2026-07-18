from src.labels import normalize_label


def test_normalize_label_trims_outer_space():
    assert normalize_label("  Alpha  ") == "alpha"


def test_normalize_label_collapses_repeated_spaces():
    assert normalize_label("alpha    beta") == "alpha beta"


def test_normalize_label_lowercases_mixed_ascii_case():
    assert normalize_label("MiXeD CaSe") == "mixed case"
