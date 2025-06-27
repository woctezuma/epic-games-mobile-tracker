import json
from decimal import Decimal
from pathlib import Path

from update import FORMATTED_DATA_FNAME, PLATFORMS, get_save_name, save_data_to_disk

QUANTITY = 1
TARGET_CATEGORY = "freegames"
SEPARATOR = ", "


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

    age_rating = content.get("ageRating", {}).get("ageRating", {})

    return {
        "title": content.get("title"),
        "slug": slug,
        "platform": content.get("systemSpecs").get("platform"),
        "catalog_item_id": content.get("catalogItemId"),
        "sandbox_id": purchase.get("purchasePayload", {}).get("sandboxId"),
        "offer_id": purchase.get("purchasePayload", {}).get("offerId"),
        "discount": purchase.get("discount", {}).get("discountAmountDisplay"),
        "original_price": purchase.get("discount", {})
        .get("originalPriceDisplay", "€0")
        .replace("€", ""),
        "current_price": str(Decimal(purchase.get("price", {}).get("decimalPrice"))),
        "start_date": purchase.get("purchaseStateEffectiveDate"),
        "end_date": purchase.get("discount", {}).get("discountEndDate"),
        "download_size": download_size,
        "install_size": install_size,
        "age_control": age_rating.get("ageControl"),
        "in_app_purchases": content.get("attention", {}).get("inAppPurchases")
        != "None",
        "content_descriptors": age_rating.get("contentDescriptors"),
        "interactive_elements": age_rating.get("interactiveElements"),
        "media": {e.get("imageType"): e.get("imageSrc") for e in media.values()},
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


def load_data_for_every_platform() -> list:
    all_data = []
    for platform in PLATFORMS:
        new_data = load_data_from_disk(get_save_name(platform))
        all_data.extend(new_data)

    return all_data


def main() -> None:
    data = load_data_for_every_platform()
    print(f"Loaded {len(data)} items for {SEPARATOR.join(PLATFORMS)}")

    format_all_content(data)


if __name__ == "__main__":
    main()
