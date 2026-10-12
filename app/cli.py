from decimal import Decimal

from app.container import Container
from app.domain.exceptions import InspectionRejectedError
from app.domain.models import (
    Bicycle,
    ChargingCabinet,
    DockingStation,
    ElectricBicycle,
    Helmet,
    Scooter,
)


def run_demo() -> None:
    """Demonstrate every required success and failure scenario."""

    service = Container().fleet_service()
    vehicles = [
        Scooter(
            inventory_number="SC-001",
            name="Самокат у корпуса A",
            beginner_ease=8,
            daily_energy_kwh=Decimal("1.8"),
        ),
        Bicycle(
            inventory_number="BI-001",
            name="Городской велосипед",
            beginner_ease=7,
        ),
        ElectricBicycle(
            inventory_number="EB-001",
            name="Электровелосипед",
            beginner_ease=5,
            daily_energy_kwh=Decimal("2.4"),
        ),
    ]
    things = [
        Helmet(inventory_number="HL-001", name="Шлем M"),
        DockingStation(
            inventory_number="DS-001",
            name="Док-станция",
            daily_energy_kwh=Decimal("0.4"),
        ),
        ChargingCabinet(
            inventory_number="CC-001",
            name="Зарядный шкаф",
            daily_energy_kwh=Decimal("6.0"),
        ),
    ]

    print("=== Приём транспорта после техосмотра ===")
    for vehicle in vehicles:
        service.add_vehicle(vehicle)
        print(f"ПРИНЯТ: {vehicle.name} ({vehicle.inventory_number})")

    rejected = Scooter(
        inventory_number="SC-999",
        name="Самокат с неисправной батареей",
        beginner_ease=9,
        daily_energy_kwh=Decimal("99"),
    )
    try:
        service.add_vehicle(rejected)
    except InspectionRejectedError as exception:
        print(f"ОТКЛОНЁН: {exception}")

    print("\n=== Постановка вещей на баланс ===")
    for thing in things:
        service.add_item(thing)
        print(f"УЧТЕНО: {thing.name} ({thing.inventory_number})")

    report = service.summary()
    print("\n=== Сводный отчёт ===")
    print(f"Всего объектов: {report.inventory_count}")
    print(f"Транспорт: {report.vehicle_count}; вещи: {report.thing_count}")
    print(f"Суточное энергопотребление: {report.daily_energy_kwh} кВт·ч")

    print("\n=== Транспорт для новичков ===")
    for vehicle in service.beginner_vehicles():
        print(f"{vehicle.name}: простота {vehicle.beginner_ease}/10")

    print("\n=== Полная инвентарная ведомость ===")
    for item in service.inventory():
        print(f"{item.name}: {item.inventory_number}")


if __name__ == "__main__":
    run_demo()
