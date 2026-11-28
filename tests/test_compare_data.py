from compare_data import get_message_for_discord, is_key_relevant, is_value_relevant
from src.constants import CURRENCY_SYMBOL, DISCORD_ANDROID_HEADER, DISCORD_IOS_HEADER


def make_element() -> dict:
    return {
        "platform": "android",
        "title": "Example Game",
        "original_price": "19.99",
        "end_date": "2025-06-12T17:00:00.000Z",
        "media": {"OfferImageWide": "https://example.com/wide.jpg"},
    }


def test_is_key_relevant() -> None:
    assert is_key_relevant("title")
    assert not is_key_relevant("platform")


def test_is_value_relevant() -> None:
    assert is_value_relevant("x")
    assert not is_value_relevant(None)


def test_message_for_android() -> None:
    message, urls = get_message_for_discord(make_element(), verbose=False)
    assert message.startswith(DISCORD_ANDROID_HEADER)
    assert f"`original_price`: 19.99 {CURRENCY_SYMBOL}" in message
    assert "`end_date`: 2025-06-12" in message
    assert "T17:00" not in message
    assert "OfferImageWide" in message
    assert urls == {"https://example.com/wide.jpg"}


def test_message_for_ios() -> None:
    element = make_element()
    element["platform"] = "ios"
    message, _ = get_message_for_discord(element, verbose=False)
    assert message.startswith(DISCORD_IOS_HEADER)


def test_media_urls_are_deduplicated() -> None:
    element = make_element()
    _, urls = get_message_for_discord(element, verbose=False)
    message, urls = get_message_for_discord(element, urls, verbose=False)
    assert message.count("OfferImageWide") == 0
    assert urls == {"https://example.com/wide.jpg"}
