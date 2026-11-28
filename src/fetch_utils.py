import json
import os
import time

import cloudscraper
import requests

from src.constants import BASE_URL, DEFAULT_COUNTRY, PLATFORMS, START_INDEX
from src.disk_utils import get_save_name, save_data_to_disk
from src.trim_utils import remove_noisy_values

REQUEST_TIMEOUT_IN_SECONDS = 30
MAX_ATTEMPTS = 3
RETRY_DELAY_IN_SECONDS = 5


def get_default_params(platform: str, start_index: int = START_INDEX) -> dict[str, str]:
    return {
        "count": "10",
        "country": os.getenv("COUNTRY", DEFAULT_COUNTRY),
        "locale": "en",
        "platform": platform,
        "start": str(start_index),
        "store": "EGS",
    }


def fetch_data_once(
    params: dict[str, str],
    scraper: cloudscraper.CloudScraper,
) -> tuple[list, dict]:
    try:
        response = scraper.get(
            url=BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_IN_SECONDS,
        )
        response.raise_for_status()
        text = response.content.decode("utf-8")
        parsed_response = json.loads(text)
        data = parsed_response["data"]
        paging = parsed_response["paging"]
    except (requests.RequestException, ValueError, KeyError) as e:
        msg = f"Request to {BASE_URL} with params {params} failed: {e}"
        raise RuntimeError(msg) from e
    else:
        return data, paging


def fetch_data_for_platform_and_start_index(
    platform: str,
    start_index: int,
    scraper: cloudscraper.CloudScraper | None = None,
) -> tuple[list, dict]:
    if scraper is None:
        scraper = cloudscraper.create_scraper()

    params = get_default_params(platform, start_index)

    last_error: RuntimeError | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fetch_data_once(params, scraper)
        except RuntimeError as e:
            last_error = e
            print(
                f"Attempt {attempt}/{MAX_ATTEMPTS} failed for {platform} "
                f"at index {start_index}: {e}",
            )
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY_IN_SECONDS * attempt)

    msg = (
        f"Failed to fetch data for {platform} at index {start_index} "
        f"after {MAX_ATTEMPTS} attempts"
    )
    raise RuntimeError(msg) from last_error


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
