from __future__ import annotations

from typing import Any

import allure
import pytest
import requests

from allure_helpers import attach_json, attach_response, normalize_item_payload, normalize_stats_payload
from data_factory import generate_payload


def assert_item_structure(item: dict[str, Any]) -> None:
    required_fields = {"id", "sellerId", "name", "price", "statistics", "createdAt"}
    missing = required_fields - set(item)
    assert not missing, f"Missing fields in item response: {missing}"

    assert isinstance(item["id"], str) and item["id"], "Field 'id' must be a non-empty string."
    assert isinstance(item["sellerId"], int), "Field 'sellerId' must be int."
    assert isinstance(item["name"], str) and item["name"], "Field 'name' must be a non-empty string."
    assert isinstance(item["price"], int), "Field 'price' must be int."
    assert isinstance(item["statistics"], dict), "Field 'statistics' must be dict."
    assert isinstance(item["createdAt"], str) and item["createdAt"], (
        "Field 'createdAt' must be a non-empty string."
    )

    assert_stats_structure(item["statistics"])


def assert_stats_structure(stats: dict[str, Any]) -> None:
    required_fields = {"likes", "viewCount", "contacts"}
    missing = required_fields - set(stats)
    assert not missing, f"Missing fields in statistics response: {missing}"

    for field_name in required_fields:
        value = stats[field_name]
        assert isinstance(value, int), f"Field '{field_name}' must be int."
        assert value >= 0, f"Field '{field_name}' must be non-negative."


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Positive scenarios")
@allure.title("Create item with valid data")
@allure.description(
    "Checks that the service creates an item, returns HTTP 200 and a valid response body."
)
@pytest.mark.smoke
@pytest.mark.contract
def test_create_item_with_valid_data(api_client: requests.Session, unique_seller_id: int) -> None:
    payload = generate_payload(seller_id=unique_seller_id)

    with allure.step("Send POST /api/1/item with valid payload"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 200
    body = response.json()
    assert_item_structure(body)
    assert body["sellerId"] == payload["sellerID"]
    assert body["name"] == payload["name"]
    assert body["price"] == payload["price"]


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Positive scenarios")
@allure.title("Create two items with identical business data")
@allure.description(
    "Checks non-idempotent behavior for item creation: identical payloads should produce different ids."
)
@pytest.mark.smoke
def test_create_two_items_with_same_payload_returns_different_ids(
    api_client: requests.Session,
    unique_seller_id: int,
) -> None:
    payload = generate_payload(seller_id=unique_seller_id)

    with allure.step("Create first item"):
        attach_json("payload_first", payload)
        first_response = api_client.create_item(payload)
        attach_response(first_response, "first_response")

    with allure.step("Create second item with the same payload"):
        second_response = api_client.create_item(payload)
        attach_response(second_response, "second_response")

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_body = first_response.json()
    second_body = second_response.json()

    assert first_body["id"] != second_body["id"]


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item without sellerID")
@allure.description("Checks validation for missing sellerID.")
@pytest.mark.negative
def test_create_item_without_seller_id_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload()
    payload.pop("sellerID")

    with allure.step("Send POST /api/1/item without sellerID"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item without name")
@allure.description("Checks validation for missing name.")
@pytest.mark.negative
def test_create_item_without_name_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload()
    payload.pop("name")

    with allure.step("Send POST /api/1/item without name"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item without price")
@allure.description("Checks validation for missing price.")
@pytest.mark.negative
def test_create_item_without_price_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload()
    payload.pop("price")

    with allure.step("Send POST /api/1/item without price"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item with string sellerID")
@allure.description("Checks validation for incorrect sellerID data type.")
@pytest.mark.negative
def test_create_item_with_string_seller_id_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload()
    payload["sellerID"] = "555555"

    with allure.step("Send POST /api/1/item with string sellerID"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item with string price")
@allure.description("Checks validation for incorrect price data type.")
@pytest.mark.negative
def test_create_item_with_string_price_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload()
    payload["price"] = "1000"

    with allure.step("Send POST /api/1/item with string price"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("POST /api/1/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Create item with negative price")
@allure.description("Checks validation for negative price.")
@pytest.mark.negative
def test_create_item_with_negative_price_returns_400(api_client: requests.Session) -> None:
    payload = generate_payload(price=-1)

    with allure.step("Send POST /api/1/item with negative price"):
        attach_json("payload", payload)
        response = api_client.create_item(payload)
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/item/{id}")
@allure.sub_suite("Positive scenarios")
@allure.title("Get item by existing id")
@allure.description("Checks that a previously created item can be fetched by id.")
@pytest.mark.smoke
@pytest.mark.e2e
def test_get_item_by_existing_id(created_item: dict[str, Any], api_client: requests.Session) -> None:
    item_id = created_item["item_id"]
    request_payload = created_item["request_payload"]

    with allure.step("Send GET /api/1/item/{id}"):
        response = api_client.get_item_by_id(item_id)
        attach_response(response)

    assert response.status_code == 200
    item = normalize_item_payload(response.json())
    assert_item_structure(item)
    assert item["id"] == item_id
    assert item["sellerId"] == request_payload["sellerID"]
    assert item["name"] == request_payload["name"]
    assert item["price"] == request_payload["price"]


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/item/{id}")
@allure.sub_suite("Negative scenarios")
@allure.title("Get item by non-existing id")
@allure.description("Checks that the API returns 404 for a non-existing item id.")
@pytest.mark.negative
def test_get_item_by_non_existing_id_returns_404(api_client: requests.Session) -> None:
    non_existing_id = "99999999-qa-non-existing-id"

    with allure.step("Send GET /api/1/item/{id} with non-existing id"):
        response = api_client.get_item_by_id(non_existing_id)
        attach_response(response)

    assert response.status_code == 404


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/item/{id}")
@allure.sub_suite("Negative scenarios")
@allure.title("Get item by invalid id format")
@allure.description("Checks validation for invalid id format.")
@pytest.mark.negative
def test_get_item_by_invalid_id_returns_400(api_client: requests.Session) -> None:
    with allure.step("Send GET /api/1/item/invalid_id"):
        response = api_client.get_item_by_id("invalid_id")
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/{sellerID}/item")
@allure.sub_suite("Positive scenarios")
@allure.title("Get seller items by valid sellerID")
@allure.description("Checks that the created item is returned in the seller item list.")
@pytest.mark.smoke
@pytest.mark.e2e
def test_get_items_by_seller_returns_created_item(
    created_item: dict[str, Any],
    api_client: requests.Session,
) -> None:
    seller_id = created_item["seller_id"]
    item_id = created_item["item_id"]

    with allure.step("Send GET /api/1/{sellerID}/item"):
        response = api_client.get_items_by_seller(seller_id)
        attach_response(response)

    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list), "Expected list response for seller items."
    assert any(item.get("id") == item_id for item in items), "Created item was not found in seller list."
    assert all(item.get("sellerId") == seller_id for item in items), (
        "At least one item in seller list belongs to another seller."
    )


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/{sellerID}/item")
@allure.sub_suite("Negative scenarios")
@allure.title("Get seller items by invalid sellerID format")
@allure.description("Checks validation for invalid sellerID format in path.")
@pytest.mark.negative
def test_get_items_by_invalid_seller_id_returns_400(api_client: requests.Session) -> None:
    with allure.step("Send GET /api/1/invalid/item"):
        response = api_client.get_items_by_seller("invalid")
        attach_response(response)

    assert response.status_code == 400


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/statistic/{id}")
@allure.sub_suite("Positive scenarios")
@allure.title("Get statistics v1 by existing item id")
@allure.description("Checks that v1 statistic endpoint returns valid statistics for a created item.")
@pytest.mark.smoke
@pytest.mark.e2e
def test_get_statistics_v1_by_existing_id(
    created_item: dict[str, Any],
    api_client: requests.Session,
) -> None:
    item_id = created_item["item_id"]

    with allure.step("Send GET /api/1/statistic/{id}"):
        response = api_client.get_statistic_v1(item_id)
        attach_response(response)

    assert response.status_code == 200
    stats = normalize_stats_payload(response.json())
    assert_stats_structure(stats)


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/1/statistic/{id}")
@allure.sub_suite("Negative scenarios")
@allure.title("Get statistics v1 by non-existing item id")
@allure.description("Checks that v1 statistic endpoint returns 404 for a non-existing item id.")
@pytest.mark.negative
def test_get_statistics_v1_by_non_existing_id_returns_404(
    api_client: requests.Session,
) -> None:
    with allure.step("Send GET /api/1/statistic/{id} with non-existing id"):
        response = api_client.get_statistic_v1("99999999-qa-non-existing-id")
        attach_response(response)

    assert response.status_code == 404


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/2/statistic/{id}")
@allure.sub_suite("Positive scenarios")
@allure.title("Get statistics v2 by existing item id")
@allure.description("Checks that v2 statistic endpoint returns valid statistics for a created item.")
@pytest.mark.smoke
@pytest.mark.e2e
def test_get_statistics_v2_by_existing_id(
    created_item: dict[str, Any],
    api_client: requests.Session,
) -> None:
    item_id = created_item["item_id"]

    with allure.step("Send GET /api/2/statistic/{id}"):
        response = api_client.get_statistic_v2(item_id)
        attach_response(response)

    assert response.status_code == 200
    stats = normalize_stats_payload(response.json())
    assert_stats_structure(stats)


@allure.parent_suite("Avito QA Internship API")
@allure.suite("GET /api/2/statistic/{id}")
@allure.sub_suite("Version comparison")
@allure.title("Compare statistics v1 and v2 for the same item")
@allure.description("Checks that v1 and v2 statistic endpoints return consistent business data.")
@pytest.mark.contract
@pytest.mark.e2e
def test_statistics_v1_and_v2_are_consistent(
    created_item: dict[str, Any],
    api_client: requests.Session,
) -> None:
    item_id = created_item["item_id"]

    with allure.step("Request statistics from v1"):
        response_v1 = api_client.get_statistic_v1(item_id)
        attach_response(response_v1, "statistics_v1")

    with allure.step("Request statistics from v2"):
        response_v2 = api_client.get_statistic_v2(item_id)
        attach_response(response_v2, "statistics_v2")

    assert response_v1.status_code == 200
    assert response_v2.status_code == 200

    stats_v1 = normalize_stats_payload(response_v1.json())
    stats_v2 = normalize_stats_payload(response_v2.json())

    assert stats_v1 == stats_v2, "Statistics returned by v1 and v2 are inconsistent."
