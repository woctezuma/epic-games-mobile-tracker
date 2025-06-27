import requests

from src.disk_utils import load_discord_webhook

DISCORD_API_URL = "https://discord.com/api/webhooks/"
TIMEOUT_IN_SECONDS = 5


def get_webhook_id(webhook_keyword: str = "id") -> str:
    webhook = load_discord_webhook()
    return webhook.get(webhook_keyword)


def get_webhook_url(webhook_id: str) -> str:
    return f"{DISCORD_API_URL}{webhook_id}"


def post_message_to_discord(
    message: str,
    webhook_id: str | None,
) -> requests.Response | None:
    if webhook_id is None or len(message) == 0:
        response = None
    else:
        json_data = {"content": message}
        response = requests.post(
            url=get_webhook_url(webhook_id),
            json=json_data,
            timeout=TIMEOUT_IN_SECONDS,
        )

    return response


def post_message_to_discord_using_keyword(
    message: str,
    webhook_keyword: str,
) -> requests.Response | None:
    return post_message_to_discord(message, get_webhook_id(webhook_keyword))
