import json
from pathlib import Path


def load_json(fname: str) -> dict:
    with Path(fname).open(encoding="utf8") as f:
        return json.load(f)


def load_json_failsafe(fname: str) -> dict:
    try:
        data = load_json(fname)
    except FileNotFoundError:
        data = {}
    return data


def save_json(data: dict, fname: str, *, prettify: bool = False) -> None:
    Path(fname).parent.mkdir(parents=True, exist_ok=True)

    with Path(fname).open("w", encoding="utf8") as f:
        if prettify:
            json.dump(data, f, indent=2, sort_keys=True)
        else:
            json.dump(data, f)
