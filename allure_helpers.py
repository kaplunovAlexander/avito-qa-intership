from __future__ import annotations

import json
from typing import Any

import allure
import requests


def attach_json(name: str, data: Any) -> None:
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(response: requests.Response, name: str = "response") -> None:
    try:
        body = response.json()
    except ValueError:
        body = response.text

    attach_json(
        name,
        {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
            "elapsed_ms": int(response.elapsed.total_seconds() * 1000),
            "url": response.url,
        },
    )


def normalize_item_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        if not payload:
            raise AssertionError("Expected a non-empty item list, got an empty list.")
        return payload[0]
    if isinstance(payload, dict):
        return payload
    raise AssertionError(f"Unexpected item response type: {type(payload)!r}")


def normalize_stats_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        if not payload:
            raise AssertionError("Expected a non-empty statistics list, got an empty list.")
        return payload[0]
    if isinstance(payload, dict):
        return payload
    raise AssertionError(f"Unexpected statistics response type: {type(payload)!r}")
