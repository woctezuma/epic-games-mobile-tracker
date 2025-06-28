from src.constants import (
    CURRENCY_SYMBOL,
    DISCORD_ANDROID_HEADER,
    DISCORD_IOS_HEADER,
    LINEBREAK,
    PLATFORMS,
    SEPARATOR,
    WEBHOOK_KEYWORD_MOBILE,
)
from src.discord_utils import post_message_to_discord_using_keyword
from src.disk_utils import load_data_for_every_platform
from src.format_utils import format_all_content

FIELDS_OF_INTEREST = [
    "title",
    "store_url",
    "checkout_url",
    "original_price",
    "discount",
    "end_date",
    "media",
]

TIME_SEPARATOR = "T"
NUM_SPACES = 3
INDENT_SPACE = " " * NUM_SPACES


def is_key_relevant(key: str) -> bool:
    return not FIELDS_OF_INTEREST or key in FIELDS_OF_INTEREST


def is_value_relevant(value: str) -> bool:
    return value is not None


def main() -> None:
    data = load_data_for_every_platform()
    print(f"Loaded {len(data)} items for {SEPARATOR.join(PLATFORMS)}")

    d = format_all_content(data)

    urls = set()

    for e in d.values():
        if e.get("platform") == "android":
            message = DISCORD_ANDROID_HEADER
        else:
            message = DISCORD_IOS_HEADER

        media = e.get("media", {})

        media_message = f"{LINEBREAK} `media`:"
        for k in sorted(media):
            url = media[k]
            if url not in urls:
                urls.add(url)
                media_message += f"\n{INDENT_SPACE}- `{k}`: {media[k]}"

        for k, v in e.items():
            if k == "media":
                message += media_message
            elif is_key_relevant(k) and is_value_relevant(v):
                line = f"{LINEBREAK} `{k}`: {v}"
                if "price" in k:
                    line += f" {CURRENCY_SYMBOL}"
                elif "date" in k:
                    line = line.rsplit(TIME_SEPARATOR)[0]
                message += line

        print(message)
        post_message_to_discord_using_keyword(
            message,
            webhook_keyword=WEBHOOK_KEYWORD_MOBILE,
        )


if __name__ == "__main__":
    main()
