from __future__ import annotations

from typing import Any

import requests


class ApiClient:
    BASE_URL = "https://qa-internship.avito.com"

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def create_item(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(
            f"{self.BASE_URL}/api/1/item",
            json=payload,
            timeout=self.timeout,
        )

    def get_item_by_id(self, item_id: str) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/api/1/item/{item_id}",
            timeout=self.timeout,
        )

    def get_items_by_seller(self, seller_id: int | str) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/api/1/{seller_id}/item",
            timeout=self.timeout,
        )

    def get_statistic_v1(self, item_id: str) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/api/1/statistic/{item_id}",
            timeout=self.timeout,
        )

    def get_statistic_v2(self, item_id: str) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/api/2/statistic/{item_id}",
            timeout=self.timeout,
        )
