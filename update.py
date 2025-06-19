import json

import cloudscraper

HOST = "https://egs-platform-service.store.epicgames.com"
ENDPOINT = "/api/v2/public/discover/home"
BASE_URL = f"{HOST}{ENDPOINT}"

PLATFORMS = ["android", "ios"]
START_INDEX = 0

PARAMS = {
    "count": "10",
    "country": "US",
    "locale": "en",
    "platform": PLATFORMS[0],
    "start": START_INDEX,
    "store": "EGS",
}

scraper = cloudscraper.create_scraper()
response = scraper.get(url=BASE_URL, params=PARAMS)
text = response.content.decode("utf-8")
parsed_data = json.loads(text)
