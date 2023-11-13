from hassil.edit_distance import edit_distance


def test_same_string() -> None:
    assert edit_distance("test", "test") == 0


def test_different_strings() -> None:
    assert edit_distance("1234", "5678") == 4


def test_substitutions() -> None:
    assert edit_distance("1234", "1244") == 1
    assert edit_distance("1234", "1244", substitution_cost=3) == 2
    assert edit_distance("1234", "4444", substitution_cost=3) == 6
