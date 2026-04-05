from __future__ import annotations

import random
import uuid
from typing import Any


def generate_seller_id() -> int:
    return random.randint(111111, 999999)


def generate_payload(
    *,
    seller_id: int | None = None,
    name: str | None = None,
    price: int = 1000,
    likes: int = 1,
    view_count: int = 10,
    contacts: int = 2,
) -> dict[str, Any]:
    unique_suffix = uuid.uuid4().hex[:8]
    return {
        "sellerID": seller_id if seller_id is not None else generate_seller_id(),
        "name": name or f"qa-item-{unique_suffix}",
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
