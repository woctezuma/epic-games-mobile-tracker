import json

import cloudscraper

from src.constants import BASE_URL, PLATFORMS, START_INDEX
from src.disk_utils import get_save_name, save_data_to_disk
from src.trim_utils import remove_noisy_values


def get_default_params(platform: str, start_index: int = START_INDEX) -> dict[str, str]:
    return {
        "count": "10",
        "country": "FR",
        "locale": "en",
        "platform": platform,
        "start": str(start_index),
        "store": "EGS",
    }


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
        data = remove_noisy_values(data)
        print(f"Saving data for {platform} to disk. Total items: {len(data)}")
        save_data_to_disk(data, get_save_name(platform))

    return data


def fetch_data_for_every_platform() -> list:
    scraper = cloudscraper.create_scraper()
    all_data = []
    for platform in PLATFORMS:
        new_data = fetch_data_for_platform(platform, scraper)
        all_data.extend(new_data)

    return all_data
