from src.constants import (
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

        media_message = ""
        for k in sorted(media):
            url = media[k]
            if url not in urls:
                urls.add(url)
                media_message += f"{LINEBREAK} `{k}`: {media[k]}"

        for k, v in e.items():
            if k == "media":
                message += media_message
            elif v and v != "0":
                message += f"{LINEBREAK} `{k}`: {v}"

        print(message)
        post_message_to_discord_using_keyword(
            message,
            webhook_keyword=WEBHOOK_KEYWORD_MOBILE,
        )


if __name__ == "__main__":
    main()
