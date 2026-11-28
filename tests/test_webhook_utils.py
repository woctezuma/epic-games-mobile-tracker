from src.webhook_utils import filter_dict_by_key, format_dict_keys, format_key


def test_filter_dict_by_key() -> None:
    env = {"DISCORD_MOBILE": "url", "OTHER": "x"}
    assert filter_dict_by_key(env, "DISCORD_") == {"DISCORD_MOBILE": "url"}


def test_format_key() -> None:
    assert format_key("DISCORD_MOBILE", "DISCORD_") == "mobile"


def test_format_dict_keys() -> None:
    env = {"DISCORD_MOBILE": "url"}
    assert format_dict_keys(env, "DISCORD_") == {"mobile": "url"}
