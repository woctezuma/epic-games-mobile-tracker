from src.trim_utils import remove_noisy_values


def test_remove_noisy_values_from_dict() -> None:
    data = {
        "a": 1,
        "purchaseStateEffectiveDate": "2025-01-01",
        "nested": {"purchaseStateEffectiveDate": "x", "b": 2},
    }
    assert remove_noisy_values(data) == {"a": 1, "nested": {"b": 2}}


def test_remove_noisy_values_from_list() -> None:
    data = [{"purchaseStateEffectiveDate": "x"}, {"keep": True}]
    assert remove_noisy_values(data) == [{}, {"keep": True}]
