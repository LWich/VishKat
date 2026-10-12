from fastapi.testclient import TestClient


def test_api_accepts_every_supported_transport_and_item_type(client: TestClient) -> None:
    payloads: list[tuple[str, dict[str, object]]] = [
        (
            "/api/v1/vehicles",
            {
                "type": "bicycle",
                "inventory_number": "BI-ALL",
                "name": "Велосипед",
                "beginner_ease": 6,
            },
        ),
        (
            "/api/v1/vehicles",
            {
                "type": "electric_bicycle",
                "inventory_number": "EB-ALL",
                "name": "Электровелосипед",
                "beginner_ease": 7,
                "daily_energy_kwh": "4.2",
            },
        ),
        (
            "/api/v1/items",
            {
                "type": "docking_station",
                "inventory_number": "DS-ALL",
                "name": "Док-станция",
                "daily_energy_kwh": "0.4",
            },
        ),
        (
            "/api/v1/items",
            {
                "type": "charging_cabinet",
                "inventory_number": "CC-ALL",
                "name": "Зарядный шкаф",
                "daily_energy_kwh": "6.0",
            },
        ),
    ]

    for path, payload in payloads:
        response = client.post(path, json=payload)
        assert response.status_code == 201
        assert response.json()["type"] == payload["type"]

    assert client.get("/api/v1/reports/summary").json() == {
        "inventory_count": 4,
        "vehicle_count": 2,
        "thing_count": 2,
        "daily_energy_kwh": "10.6",
    }


def test_full_api_scenario(client: TestClient) -> None:
    vehicle_response = client.post(
        "/api/v1/vehicles",
        json={
            "type": "scooter",
            "inventory_number": "SC-API-1",
            "name": "API-самокат",
            "beginner_ease": 8,
            "daily_energy_kwh": "2.5",
        },
    )
    item_response = client.post(
        "/api/v1/items",
        json={
            "type": "helmet",
            "inventory_number": "HL-API-1",
            "name": "API-шлем",
        },
    )

    assert vehicle_response.status_code == 201
    assert vehicle_response.json() == {
        "type": "scooter",
        "inventory_number": "SC-API-1",
        "name": "API-самокат",
        "beginner_ease": 8,
        "daily_energy_kwh": "2.5",
    }
    assert item_response.status_code == 201
    assert item_response.json() == {
        "type": "helmet",
        "inventory_number": "HL-API-1",
        "name": "API-шлем",
        "beginner_ease": None,
        "daily_energy_kwh": None,
    }
    assert client.get("/api/v1/health").json() == {"status": "ok"}
    assert client.get("/api/v1/reports/summary").json() == {
        "inventory_count": 2,
        "vehicle_count": 1,
        "thing_count": 1,
        "daily_energy_kwh": "2.5",
    }
    beginner = client.get("/api/v1/vehicles/beginner").json()
    assert [item["inventory_number"] for item in beginner] == ["SC-API-1"]
    assert len(client.get("/api/v1/inventory").json()) == 2


def test_api_returns_422_for_failed_inspection(client: TestClient) -> None:
    response = client.post(
        "/api/v1/vehicles",
        json={
            "type": "electric_bicycle",
            "inventory_number": "EB-BROKEN",
            "name": "Неисправный электровелосипед",
            "beginner_ease": 9,
            "daily_energy_kwh": "99",
        },
    )
    assert response.status_code == 422
    assert "failed inspection" in response.json()["detail"]


def test_api_returns_409_for_duplicate_number(client: TestClient) -> None:
    payload = {
        "type": "helmet",
        "inventory_number": "HL-DUP",
        "name": "Шлем",
    }
    assert client.post("/api/v1/items", json=payload).status_code == 201
    assert client.post("/api/v1/items", json=payload).status_code == 409


def test_api_returns_400_for_whitespace_only_domain_value(client: TestClient) -> None:
    response = client.post(
        "/api/v1/items",
        json={
            "type": "helmet",
            "inventory_number": "HL-BLANK",
            "name": "   ",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Name must not be blank"}


def test_openapi_metadata(client: TestClient) -> None:
    info = client.get("/openapi.json").json()["info"]
    assert info["title"] == "VyshKat API"
    assert info["version"] == "1.0.0"
