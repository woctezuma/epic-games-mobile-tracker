from src.constants import TARGET_PREFIX, WEBHOOK_FNAME
from src.json_utils import save_json
from src.webhook_utils import filter_dict_by_key, format_dict_keys, get_environment


def main() -> None:
    environment = filter_dict_by_key(get_environment(), TARGET_PREFIX)
    discord_webhooks = format_dict_keys(environment, TARGET_PREFIX)
    save_json(discord_webhooks, WEBHOOK_FNAME)


if __name__ == "__main__":
    main()
