import json
from pathlib import Path

from src.constants import DATA_FOLDER, FORMATTED_DATA_FNAME, PLATFORMS, WEBHOOK_FNAME
from src.json_utils import load_json_failsafe


def load_discord_webhook() -> dict:
    return load_json_failsafe(WEBHOOK_FNAME)


def get_save_name(platform: str) -> str:
    return f"{DATA_FOLDER}/{platform}.json"


def save_data_to_disk(data: list | dict, fname: str) -> None:
    with Path(fname).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True, ensure_ascii=False)


def load_data_from_disk(fname: str) -> list:
    with Path(fname).open("r", encoding="utf-8") as file:
        return json.load(file)


def load_data_for_every_platform() -> list:
    all_data = []
    for platform in PLATFORMS:
        new_data = load_data_from_disk(get_save_name(platform))
        all_data.extend(new_data)

    return all_data


def load_old_formatted_data() -> dict:
    return load_json_failsafe(get_save_name(FORMATTED_DATA_FNAME))
