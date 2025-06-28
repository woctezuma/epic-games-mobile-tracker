from decimal import Decimal

from src.constants import (
    CURRENCY_SYMBOL,
    FORMATTED_DATA_FNAME,
    QUANTITY,
    TARGET_CATEGORY,
)
from src.disk_utils import get_save_name, save_data_to_disk

STORE_BASE_URL = "https://store.epicgames.com/product/"
CHECKOUT_BASE_URL = "https://store.epicgames.com/purchase?offers="


def get_store_url(slug: str) -> str:
    return f"<{STORE_BASE_URL}{slug}>"


def build_id(sandbox_id: str, offer_id: str) -> str:
    return f"{QUANTITY}-{sandbox_id}-{offer_id}"


def get_checkout_url(sandbox_id: str, offer_id: str) -> str:
    return f"<{CHECKOUT_BASE_URL}{build_id(sandbox_id, offer_id)}>"


def format_content(content: dict) -> dict:
    media = content.get("media", {})
    slug = content.get("mapping", {}).get("slug")

    purchases = [
        e for e in content.get("purchase", []) if e.get("purchaseType") == "Claim"
    ]

    if not purchases:
        print(f"- Skipping {slug}")
        return {}

    purchase = purchases[0]

    if len(purchases) > 1:
        msg = f"Expected exactly one purchase of type 'Claim', found {len(purchases)}"
        raise ValueError(
            msg,
        )

    system_specs = content.get("systemSpecs", {})
    system_requirements = system_specs.get("systemRequirements", [])
    download_size = None
    install_size = None
    for e in system_requirements:
        if e["requirementType"] == "DownloadSize":
            download_size = e["minimum"]
        elif e["requirementType"] == "InstallSize":
            install_size = e["minimum"]

    discount = purchase.get("discount", {})
    age_rating = content.get("ageRating", {}).get("ageRating", {})

    sandbox_id = purchase.get("purchasePayload", {}).get("sandboxId")
    offer_id = purchase.get("purchasePayload", {}).get("offerId")

    return {
        "title": content.get("title"),
        "slug": slug,
        "platform": system_specs.get("platform"),
        "catalog_item_id": content.get("catalogItemId"),
        "sandbox_id": sandbox_id,
        "offer_id": offer_id,
        "store_url": get_store_url(slug),
        "checkout_url": get_checkout_url(sandbox_id, offer_id),
        "original_price": str(
            Decimal(
                discount.get("originalPriceDisplay", f"{CURRENCY_SYMBOL}0").replace(
                    CURRENCY_SYMBOL,
                    "",
                ),
            ),
        ),
        "current_price": str(Decimal(purchase.get("price", {}).get("decimalPrice"))),
        "discount": discount.get("discountAmountDisplay"),
        "start_date": purchase.get("purchaseStateEffectiveDate"),
        "end_date": discount.get("discountEndDate"),
        "download_size": download_size,
        "install_size": install_size,
        "age_control": age_rating.get("ageControl"),
        "in_app_purchases": content.get("attention", {}).get("inAppPurchases")
        != "None",
        "content_descriptors": age_rating.get("contentDescriptors"),
        "interactive_elements": age_rating.get("interactiveElements"),
        "media": {
            e.get("imageType"): e.get("imageSrc")
            for e in sorted(media.values(), key=lambda x: x.get("imageType", ""))
        },
    }


def format_all_content(data: list, *, save_to_disk: bool = True) -> dict:
    offers = []
    for collection in data:
        offers += collection.get("offers", [])

    d = {}
    for offer in sorted(
        offers,
        key=lambda x: x.get("content", {}).get("mapping", {}).get("slug", ""),
    ):
        sandbox_id = offer["sandboxId"]
        offer_id = offer["offerId"]
        content = offer.get("content", {})

        if TARGET_CATEGORY in content.get("categories", []):
            k = build_id(sandbox_id, offer_id)
            v = format_content(content)

            if v:
                print(f"+ Adding {v['slug']}")
                d[k] = v

    print(f"Found {len(d)} items in category '{TARGET_CATEGORY}'")

    if save_to_disk:
        print("Saving formatted data to disk. Total items:", len(d))
        save_data_to_disk(d, get_save_name(FORMATTED_DATA_FNAME))

    return d
