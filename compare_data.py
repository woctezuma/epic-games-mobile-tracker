import json
from pathlib import Path

from update import ALL_PLATFORMS, get_save_name

QUANTITY = 1
TARGET_CATEGORY = "freegames"


def load_data_from_disk(fname: str) -> list:
    with Path(fname).open("r", encoding="utf-8") as file:
        return json.load(file)


def build_id(sandbox_id: str, offer_id: str) -> str:
    return f"{QUANTITY}-{sandbox_id}-{offer_id}"


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

    system_requirements = content.get("systemSpecs", {}).get("systemRequirements", [])
    download_size = None
    install_size = None
    for e in system_requirements:
        if e["requirementType"] == "DownloadSize":
            download_size = e["minimum"]
        elif e["requirementType"] == "InstallSize":
            install_size = e["minimum"]

    return {
        "ageRating": content.get("ageRating", {})
        .get("ageRating", {})
        .get("ageControl"),
        "inAppPurchases": content.get("attention", {}).get("inAppPurchases"),
        "catalogItemId": content.get("catalogItemId"),
        "slug": slug,
        "title": content.get("title"),
        "platform": content.get("platform"),
        "media": {e.get("imageType"): e.get("imageSrc") for e in media.values()},
        "offerId": purchase.get("purchasePayload", {}).get("offerId"),
        "sandboxId": purchase.get("purchasePayload", {}).get("sandboxId"),
        "start_date": purchase.get("purchaseStateEffectiveDate"),
        "end_date": purchase.get("discount", {}).get("discountEndDate"),
        "discount": purchase.get("discount", {}).get("discountAmountDisplay"),
        "original_price": purchase.get("discount", {}).get("originalPriceDisplay"),
        "price": purchase.get("price", {}).get("decimalPrice"),
        "download_size": download_size,
        "install_size": install_size,
    }


def main() -> None:
    data = load_data_from_disk(get_save_name(ALL_PLATFORMS))
    print(f"Loaded {len(data)} items from {get_save_name(ALL_PLATFORMS)}")

    d = {}
    for collection in data:
        for offer in collection.get("offers", []):
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


if __name__ == "__main__":
    main()
