from src.constants import PLATFORMS, SEPARATOR
from src.disk_utils import load_data_for_every_platform
from src.format_utils import format_all_content


def main() -> None:
    data = load_data_for_every_platform()
    print(f"Loaded {len(data)} items for {SEPARATOR.join(PLATFORMS)}")

    format_all_content(data)


if __name__ == "__main__":
    main()
