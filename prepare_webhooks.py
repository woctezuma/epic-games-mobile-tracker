import os

from src.json_utils import save_json

TARGET_PREFIX = "DISCORD_"
WEBHOOK_FNAME = "data/discord_webhook.json"


def get_environment() -> os._Environ[str]:
    return os.environ


def filter_dict_by_key(d: dict[str, str], target_prefix: str) -> dict[str, str]:
    return {k: v for k, v in d.items() if k.startswith(target_prefix)}


def format_dict_keys(d: dict[str, str], target_prefix: str) -> dict[str, str]:
    return {format_key(k, target_prefix): v for k, v in d.items()}


def format_key(k: str, prefix: str) -> str:
    return k.removeprefix(prefix).lower()


def main() -> None:
    environment = filter_dict_by_key(get_environment(), TARGET_PREFIX)
    discord_webhooks = format_dict_keys(environment, TARGET_PREFIX)
    save_json(discord_webhooks, WEBHOOK_FNAME)


if __name__ == "__main__":
    main()
