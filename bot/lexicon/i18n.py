from .ru import RU
from .en import EN


def get_translations() -> dict[str, str | dict[str, str]]:
    return {
        "default": "ru",
        "en": EN,
        "ru": RU,
    }