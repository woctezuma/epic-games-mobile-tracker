from pathlib import Path
from typing import overload

from src.constants import PLATFORMS
from src.disk_utils import get_save_name, load_data_from_disk, save_data_to_disk

NOISY_FIELD = "purchaseStateEffectiveDate"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


@overload
def remove_noisy_values(data: dict) -> dict: ...
@overload
def remove_noisy_values(data: list) -> list: ...
def remove_noisy_values(data: list | dict) -> list | dict:
    if isinstance(data, dict):
        return {k: remove_noisy_values(v) for k, v in data.items() if k != NOISY_FIELD}
    if isinstance(data, list):
        return [remove_noisy_values(item) for item in data]
    return data


def main() -> None:
    for platform in PLATFORMS:
        fname = PROJECT_ROOT / get_save_name(platform)
        data = load_data_from_disk(fname)
        data = remove_noisy_values(data)
        save_data_to_disk(data, fname)


if __name__ == "__main__":
    main()
