import json
from pathlib import Path

from src.constants import DATA_FOLDER, PLATFORMS


def get_save_name(platform: str) -> str:
    return f"{DATA_FOLDER}/{platform}.json"


def save_data_to_disk(data: list | dict, fname: str) -> None:
    with Path(fname).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data_from_disk(fname: str) -> list:
    with Path(fname).open("r", encoding="utf-8") as file:
        return json.load(file)


def load_data_for_every_platform() -> list:
    all_data = []
    for platform in PLATFORMS:
        new_data = load_data_from_disk(get_save_name(platform))
        all_data.extend(new_data)

    return all_data
