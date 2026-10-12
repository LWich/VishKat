from decimal import Decimal

import pytest
from app.container import Container
from app.domain.exceptions import (
    DuplicateInventoryNumberError,
    InspectionRejectedError,
    InvalidEntityError,
)
from app.domain.models import Bicycle, ChargingCabinet, Helmet, Scooter
from dependency_injector import providers

from tests.fakes import FakeServiceCenter


def scooter(number: str = "SC-001", ease: int = 6) -> Scooter:
    return Scooter(
        inventory_number=number,
        name="Тестовый самокат",
        beginner_ease=ease,
        daily_energy_kwh=Decimal("1.25"),
    )


def test_accepts_vehicle_when_fake_inspection_approves(container: Container) -> None:
    fake = FakeServiceCenter(decision=True)
    with container.service_center.override(providers.Object(fake)):
        service = container.fleet_service()
        created = service.add_vehicle(scooter())

    assert created.inventory_number == "SC-001"
    assert fake.inspected == [created]
    assert service.summary().vehicle_count == 1


def test_rejects_vehicle_when_fake_inspection_refuses(container: Container) -> None:
    fake = FakeServiceCenter(decision=False)
    with container.service_center.override(providers.Object(fake)):
        service = container.fleet_service()
        rejected = scooter()
        with pytest.raises(InspectionRejectedError):
            service.add_vehicle(rejected)

    assert fake.inspected == [rejected]
    assert service.summary().inventory_count == 0


def test_reports_inventory_energy_and_beginner_rule(container: Container) -> None:
    fake = FakeServiceCenter(decision=True)
    with container.service_center.override(providers.Object(fake)):
        service = container.fleet_service()
        service.add_vehicle(scooter("SC-001", ease=6))
        service.add_vehicle(
            Bicycle(
                inventory_number="BI-001",
                name="Сложный велосипед",
                beginner_ease=5,
            )
        )
        service.add_item(Helmet(inventory_number="HL-001", name="Шлем"))
        service.add_item(
            ChargingCabinet(
                inventory_number="CC-001",
                name="Шкаф",
                daily_energy_kwh=Decimal("3.75"),
            )
        )

    assert service.summary().inventory_count == 4
    assert service.summary().thing_count == 2
    assert service.summary().daily_energy_kwh == Decimal("5.00")
    assert [item.inventory_number for item in service.beginner_vehicles()] == ["SC-001"]
    assert {item.inventory_number for item in service.inventory()} == {
        "SC-001",
        "BI-001",
        "HL-001",
        "CC-001",
    }


def test_rejects_duplicate_inventory_number(container: Container) -> None:
    service = container.fleet_service()
    service.add_item(Helmet(inventory_number="ONE", name="Первый шлем"))
    with pytest.raises(
        DuplicateInventoryNumberError,
        match="Inventory number 'ONE' already exists",
    ):
        service.add_item(Helmet(inventory_number="ONE", name="Второй шлем"))


@pytest.mark.parametrize("ease", [0, 11])
def test_vehicle_validates_beginner_ease(ease: int) -> None:
    with pytest.raises(InvalidEntityError):
        scooter(ease=ease)


def test_energy_cannot_be_negative() -> None:
    with pytest.raises(
        InvalidEntityError,
        match="Daily energy consumption must not be negative",
    ):
        Scooter(
            inventory_number="SC-NEG",
            name="Некорректный самокат",
            beginner_ease=8,
            daily_energy_kwh=Decimal("-1"),
        )


def test_inventory_fields_cannot_be_blank() -> None:
    with pytest.raises(InvalidEntityError, match="Inventory number"):
        Helmet(inventory_number="   ", name="Шлем")


def test_vehicle_cannot_bypass_inspection(container: Container) -> None:
    service = container.fleet_service()
    with pytest.raises(
        TypeError,
        match=r"Vehicles must be added through add_vehicle\(\) and inspected",
    ):
        service.add_item(scooter())


def test_real_service_center_accepts_energy_at_limit(container: Container) -> None:
    service = container.fleet_service()
    accepted = Scooter(
        inventory_number="SC-LIMIT",
        name="Граничный самокат",
        beginner_ease=6,
        daily_energy_kwh=Decimal("25"),
    )
    assert service.add_vehicle(accepted) is accepted


@pytest.mark.parametrize("ease", [1, 10])
def test_vehicle_accepts_beginner_ease_boundaries(ease: int) -> None:
    assert scooter(ease=ease).beginner_ease == ease


def test_zero_energy_is_valid() -> None:
    vehicle = Scooter(
        inventory_number="SC-ZERO",
        name="Самокат без расхода",
        beginner_ease=6,
        daily_energy_kwh=Decimal("0"),
    )
    assert vehicle.daily_energy_kwh == Decimal("0")


def test_empty_summary_keeps_decimal_energy_type(container: Container) -> None:
    energy = container.fleet_service().summary().daily_energy_kwh
    assert energy == Decimal("0")
    assert isinstance(energy, Decimal)
