import json
from pathlib import Path

import cloudscraper

HOST = "https://egs-platform-service.store.epicgames.com"
ENDPOINT = "/api/v2/public/discover/home"
BASE_URL = f"{HOST}{ENDPOINT}"

PLATFORMS = ["android", "ios"]
ALL_PLATFORMS = "all_platforms"
FORMATTED_DATA_FNAME = "mobile_data"
START_INDEX = 0


def get_default_params(platform: str, start_index: int = START_INDEX) -> dict[str, str]:
    return {
        "count": "10",
        "country": "FR",
        "locale": "en",
        "platform": platform,
        "start": str(start_index),
        "store": "EGS",
    }


def get_save_name(platform: str) -> str:
    return f"data/{platform}.json"


def save_data_to_disk(data: list | dict, fname: str) -> None:
    with Path(fname).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def fetch_data_for_platform_and_start_index(
    platform: str,
    start_index: int,
    scraper: cloudscraper.CloudScraper | None = None,
) -> tuple[list, dict]:
    if scraper is None:
        scraper = cloudscraper.create_scraper()

    params = get_default_params(platform, start_index)
    response = scraper.get(url=BASE_URL, params=params)
    text = response.content.decode("utf-8")
    parsed_response = json.loads(text)

    return parsed_response["data"], parsed_response["paging"]


def fetch_data_for_platform(
    platform: str,
    scraper: cloudscraper.CloudScraper | None = None,
    *,
    save_to_disk: bool = True,
) -> list:
    if scraper is None:
        scraper = cloudscraper.create_scraper()

    start_index = START_INDEX
    print(f"Fetching data for {platform} starting at index {start_index}")
    data, paging = fetch_data_for_platform_and_start_index(
        platform,
        start_index=start_index,
        scraper=scraper,
    )

    for start_index in range(
        paging["start"] + paging["count"],
        paging["total"],
        paging["count"],
    ):
        print(f"Fetching data for {platform} starting at index {start_index}")
        new_data, _ = fetch_data_for_platform_and_start_index(
            platform,
            start_index=start_index,
            scraper=scraper,
        )
        data.extend(new_data)

    if save_to_disk:
        print(f"Saving data for {platform} to disk. Total items: {len(data)}")
        save_data_to_disk(data, get_save_name(platform))

    return data


def fetch_data_for_every_platform(*, save_to_disk: bool = True) -> list:
    scraper = cloudscraper.create_scraper()
    all_data = []
    for platform in PLATFORMS:
        new_data = fetch_data_for_platform(platform, scraper)
        all_data.extend(new_data)

    if save_to_disk:
        print("Saving all data to disk. Total items:", len(all_data))
        save_data_to_disk(all_data, get_save_name(ALL_PLATFORMS))

    return all_data


def main() -> None:
    fetch_data_for_every_platform()


if __name__ == "__main__":
    main()
