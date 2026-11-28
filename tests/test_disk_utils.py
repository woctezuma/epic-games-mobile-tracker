from pathlib import Path

from src.disk_utils import get_save_name, load_data_from_disk, save_data_to_disk
from src.json_utils import load_json_failsafe, save_json


def test_get_save_name() -> None:
    assert get_save_name("android") == "data/android.json"


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    fname = tmp_path / "data.json"
    save_data_to_disk([{"b": 1, "a": 2}], fname)
    assert load_data_from_disk(fname) == [{"a": 2, "b": 1}]


def test_load_json_failsafe_missing_file(tmp_path: Path) -> None:
    assert load_json_failsafe(tmp_path / "missing.json") == {}


def test_save_json_creates_parent_dirs(tmp_path: Path) -> None:
    fname = tmp_path / "nested" / "webhook.json"
    save_json({"mobile": "url"}, fname, prettify=True)
    assert load_json_failsafe(fname) == {"mobile": "url"}
