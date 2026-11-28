import json
from pathlib import Path

import pytest

from src.format_utils import (
    build_id,
    format_all_content,
    format_content,
    get_checkout_url,
    get_store_url,
    is_both_discounted_and_claimable,
    is_categorized_as_a_giveaway,
    list_claimable_purchases,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "offer_content.json"


@pytest.fixture
def offer_content() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_build_id() -> None:
    assert build_id("sb", "of") == "1-sb-of"


def test_store_and_checkout_urls() -> None:
    assert get_store_url("slug") == "<https://store.epicgames.com/product/slug>"
    assert (
        get_checkout_url("sb", "of")
        == "<https://store.epicgames.com/purchase?offers=1-sb-of>"
    )


def test_list_claimable_purchases(offer_content: dict) -> None:
    purchases = list_claimable_purchases(offer_content)
    assert len(purchases) == 1
    assert purchases[0]["purchaseType"] == "Claim"


def test_is_both_discounted_and_claimable(offer_content: dict) -> None:
    assert is_both_discounted_and_claimable(offer_content)


def test_is_categorized_as_a_giveaway(offer_content: dict) -> None:
    assert is_categorized_as_a_giveaway(offer_content)


def test_format_content_happy_path(offer_content: dict) -> None:
    result = format_content(offer_content)
    assert result["title"] == "Example Game"
    assert result["slug"] == "example-game"
    assert result["platform"] == "Android"
    assert result["store_url"] == "<https://store.epicgames.com/product/example-game>"
    assert result["checkout_url"] == (
        "<https://store.epicgames.com/purchase?offers=1-sandbox-123-offer-123>"
    )
    assert result["original_price"] == "19.99"
    assert result["current_price"] == "0.00"
    assert result["discount"] == "€19.99"
    assert result["end_date"] == "2025-06-12T17:00:00.000Z"
    assert result["download_size"] == "1.5 GB"
    assert result["install_size"] == "3 GB"
    assert result["in_app_purchases"] is False
    assert list(result["media"]) == ["DieselGameBoxLogo", "OfferImageWide"]


def test_format_content_skips_without_claim_purchase(offer_content: dict) -> None:
    offer_content["purchase"] = []
    assert format_content(offer_content) == {}


def test_format_content_skips_with_multiple_claim_purchases(
    offer_content: dict,
) -> None:
    offer_content["purchase"].append(offer_content["purchase"][0])
    assert format_content(offer_content) == {}


def test_format_content_handles_missing_discount(offer_content: dict) -> None:
    del offer_content["purchase"][0]["discount"]
    result = format_content(offer_content)
    assert result["original_price"] == "0"
    assert result["discount"] is None
    assert result["end_date"] is None


def test_format_all_content_filters_offers(offer_content: dict) -> None:
    paid_content = {
        **offer_content,
        "title": "Paid Game",
        "categories": ["games"],
        "purchase": [
            {
                "purchaseType": "Purchase",
                "price": {"decimalPrice": "9.99"},
                "purchasePayload": {"sandboxId": "sandbox-456", "offerId": "offer-456"},
            },
        ],
    }
    collections = [
        {
            "offers": [
                {
                    "sandboxId": "sandbox-123",
                    "offerId": "offer-123",
                    "content": offer_content,
                },
                {
                    "sandboxId": "sandbox-456",
                    "offerId": "offer-456",
                    "content": paid_content,
                },
            ],
        },
    ]
    result = format_all_content(collections)
    assert list(result) == ["1-sandbox-123-offer-123"]
    assert result["1-sandbox-123-offer-123"]["title"] == "Example Game"
