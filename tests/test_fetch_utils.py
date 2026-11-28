import json
from typing import cast

import cloudscraper
import pytest
import requests

from src import fetch_utils
from src.fetch_utils import (
    MAX_ATTEMPTS,
    fetch_data_for_platform_and_start_index,
    get_default_params,
)


class FakeResponse:
    def __init__(self, payload: dict, *, ok: bool = True) -> None:
        self._payload = payload
        self._ok = ok

    def raise_for_status(self) -> None:
        if not self._ok:
            msg = "500 Server Error"
            raise requests.HTTPError(msg)

    @property
    def content(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


class BrokenResponse(FakeResponse):
    @property
    def content(self) -> bytes:
        return b"not-json"


class FakeScraper:
    def __init__(self, outcomes: list[FakeResponse | Exception]) -> None:
        self._outcomes = list(outcomes)
        self.calls = 0
        self.last_url: str | None = None
        self.last_params: dict[str, str] | None = None
        self.last_timeout: int | None = None

    def get(self, url: str, params: dict[str, str], timeout: int) -> FakeResponse:
        self.calls += 1
        self.last_url = url
        self.last_params = params
        self.last_timeout = timeout
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def no_sleep(_seconds: float) -> None:
    return None


def make_payload() -> dict:
    return {"data": [{"id": 1}], "paging": {"start": 0, "count": 10, "total": 1}}


def as_scraper(fake: FakeScraper) -> cloudscraper.CloudScraper:
    return cast("cloudscraper.CloudScraper", fake)


def test_get_default_params_uses_default_country() -> None:
    params = get_default_params("android")
    assert params["country"] == "FR"
    assert params["platform"] == "android"
    assert params["start"] == "0"


def test_get_default_params_country_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COUNTRY", "US")
    assert get_default_params("ios")["country"] == "US"


def test_fetch_succeeds_on_first_attempt() -> None:
    scraper = FakeScraper([FakeResponse(make_payload())])
    data, paging = fetch_data_for_platform_and_start_index(
        "android",
        0,
        scraper=as_scraper(scraper),
    )
    assert data == [{"id": 1}]
    assert paging["total"] == 1
    assert scraper.calls == 1
    assert scraper.last_timeout == fetch_utils.REQUEST_TIMEOUT_IN_SECONDS
    assert scraper.last_params is not None
    assert scraper.last_params["platform"] == "android"


def test_fetch_retries_until_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fetch_utils.time, "sleep", no_sleep)
    scraper = FakeScraper(
        [
            BrokenResponse({}),
            requests.ConnectionError("boom"),
            FakeResponse(make_payload()),
        ],
    )
    data, _ = fetch_data_for_platform_and_start_index(
        "ios",
        0,
        scraper=as_scraper(scraper),
    )
    assert data == [{"id": 1}]
    assert scraper.calls == 3


def test_fetch_raises_after_max_attempts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fetch_utils.time, "sleep", no_sleep)
    scraper = FakeScraper([requests.Timeout("boom")] * MAX_ATTEMPTS)
    with pytest.raises(RuntimeError, match=f"after {MAX_ATTEMPTS} attempts"):
        fetch_data_for_platform_and_start_index(
            "android",
            0,
            scraper=as_scraper(scraper),
        )
    assert scraper.calls == MAX_ATTEMPTS
