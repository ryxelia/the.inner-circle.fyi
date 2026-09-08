from datetime import date
import random


__all__: tuple[str, ...] = (
    "WEB_RING_MEMBERS",
    "get_web_ring_members",
)


WEB_RING_MEMBERS: tuple[str, ...] = (
    "abigail.sh",
    "lvh.lol", 
    "pre1ude.dev",
    "byeoon.dev",
    "azee.sh",
    "lumap.xyz",
)


def get_web_ring_members(day: date | None = None) -> tuple[str, ...]:
    """Return the ring members in a deterministic order for ``day``."""
    seed = (day or date.today()).isoformat()
    members = list(WEB_RING_MEMBERS)
    random.Random(seed).shuffle(members)
    return tuple(members)
