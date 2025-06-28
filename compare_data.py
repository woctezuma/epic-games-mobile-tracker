from src.constants import (
    CURRENCY_SYMBOL,
    DISCORD_ANDROID_HEADER,
    DISCORD_IOS_HEADER,
    FIELDS_OF_INTEREST,
    INDENT_SPACE,
    LINEBREAK,
    PLATFORMS,
    SEPARATOR,
    TIME_SEPARATOR,
    WEBHOOK_KEYWORD_MOBILE,
)
from src.discord_utils import post_message_to_discord_using_keyword
from src.disk_utils import load_data_for_every_platform, load_old_formatted_data
from src.format_utils import format_all_content


def is_key_relevant(key: str) -> bool:
    return not FIELDS_OF_INTEREST or key in FIELDS_OF_INTEREST


def is_value_relevant(value: str) -> bool:
    return value is not None


def get_message_for_discord(
    element: dict,
    urls: set | None = None,
    *,
    verbose: bool = True,
) -> str:
    if urls is None:
        urls = set()

    if element.get("platform") == "android":
        message = DISCORD_ANDROID_HEADER
    else:
        message = DISCORD_IOS_HEADER

    media = element.get("media", {})

    media_message = f"{LINEBREAK} `media`:"
    for k in sorted(media):
        url = media[k]
        if url not in urls:
            urls.add(url)
            media_message += f"\n{INDENT_SPACE}- `{k}`: {media[k]}"

    for k, v in element.items():
        if k == "media":
            message += media_message
        elif is_key_relevant(k) and is_value_relevant(v):
            line = f"{LINEBREAK} `{k}`: {v}"
            if "price" in k:
                line += f" {CURRENCY_SYMBOL}"
            elif "date" in k:
                line = line.rsplit(TIME_SEPARATOR)[0]
            message += line

    if verbose:
        print(message)

    return message, urls


def run_workflow(formatted_data: dict) -> None:
    urls = set()

    for e in formatted_data.values():
        message, urls = get_message_for_discord(e, urls)

        post_message_to_discord_using_keyword(
            message,
            webhook_keyword=WEBHOOK_KEYWORD_MOBILE,
        )


def main() -> None:
    formatted_old_data = load_old_formatted_data()

    data = load_data_for_every_platform()
    print(f"Loaded {len(data)} items for {SEPARATOR.join(PLATFORMS)}")

    formatted_data = format_all_content(data)

    formatted_diff_data = {
        k: v for k, v in formatted_data.items() if k not in formatted_old_data
    }

    run_workflow(formatted_diff_data)


if __name__ == "__main__":
    main()
