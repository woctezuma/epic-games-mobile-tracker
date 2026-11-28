import os

HOST = "https://egs-platform-service.store.epicgames.com"
ENDPOINT = "/api/v2/public/discover/home"
BASE_URL = f"{HOST}{ENDPOINT}"

PLATFORMS = ["android", "ios"]
FORMATTED_DATA_FNAME = "mobile_data"
START_INDEX = 0

QUANTITY = 1
TARGET_CATEGORY = "freegames"
SEPARATOR = ", "
DEFAULT_COUNTRY = "FR"
DEFAULT_CURRENCY_SYMBOL = "€"
CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", DEFAULT_CURRENCY_SYMBOL)

LINEBREAK = "\n-"
DISCORD_ANDROID_HEADER = "🤖👀"
DISCORD_IOS_HEADER = "🍏👀"

TARGET_PREFIX = "DISCORD_"
DATA_FOLDER = "data"
WEBHOOK_FNAME = f"{DATA_FOLDER}/discord_webhook.json"
WEBHOOK_KEYWORD_MOBILE = "mobile"

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
