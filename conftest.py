from __future__ import annotations

import random
import time
from typing import Any

import allure
import pytest
import requests

from api_client import ApiClient
from allure_helpers import attach_json, attach_response


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    return ApiClient(timeout=15)


@pytest.fixture()
def unique_seller_id() -> int:
    return random.randint(111111, 999999)


@pytest.fixture()
def created_item(api_client: ApiClient, unique_seller_id: int) -> dict[str, Any]:
    payload = {
        "sellerID": unique_seller_id,
        "name": f"qa-item-{int(time.time() * 1000)}",
        "price": 1000,
        "statistics": {
            "likes": 1,
            "viewCount": 10,
            "contacts": 2,
        },
    }

    with allure.step("Create a new item for test preconditions"):
        attach_json("create_payload", payload)
        response = api_client.create_item(payload)
        attach_response(response, "create_item_response")

    assert response.status_code == 200, (
        f"Precondition failed: unable to create item. "
        f"Expected 200, got {response.status_code}. Body: {response.text}"
    )

    body = response.json()
    item_id = body["id"]

    return {
        "request_payload": payload,
        "response_body": body,
        "item_id": item_id,
        "seller_id": unique_seller_id,
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]) -> Any:
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    exc_info = call.excinfo
    if exc_info is not None:
        allure.attach(
            str(exc_info.value),
            name="failure_message",
            attachment_type=allure.attachment_type.TEXT,
        )
