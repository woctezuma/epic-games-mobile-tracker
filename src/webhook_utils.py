import os


def get_environment() -> os._Environ[str]:
    return os.environ


def filter_dict_by_key(d: dict[str, str], target_prefix: str) -> dict[str, str]:
    return {k: v for k, v in d.items() if k.startswith(target_prefix)}


def format_dict_keys(d: dict[str, str], target_prefix: str) -> dict[str, str]:
    return {format_key(k, target_prefix): v for k, v in d.items()}


def format_key(k: str, prefix: str) -> str:
    return k.removeprefix(prefix).lower()
