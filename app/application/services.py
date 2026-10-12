from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InspectionRejectedError
from app.domain.interfaces import EnergyConsumer, FleetRepository, ServiceCenter
from app.domain.models import InventoryObject, Vehicle


@dataclass(frozen=True, slots=True)
class FleetSummary:
    inventory_count: int
    vehicle_count: int
    thing_count: int
    daily_energy_kwh: Decimal


class FleetService:
    """Coordinates fleet commands and read-only reports."""

    def __init__(
        self,
        repository: FleetRepository,
        service_center: ServiceCenter,
        beginner_threshold: int,
    ) -> None:
        self._repository = repository
        self._service_center = service_center
        self._beginner_threshold = beginner_threshold

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        if not self._service_center.accepts(vehicle):
            raise InspectionRejectedError(f"Vehicle {vehicle.inventory_number!r} failed inspection")
        self._repository.add(vehicle)
        return vehicle

    def add_item(self, item: InventoryObject) -> InventoryObject:
        if isinstance(item, Vehicle):
            raise TypeError("Vehicles must be added through add_vehicle() and inspected")
        self._repository.add(item)
        return item

    def summary(self) -> FleetSummary:
        inventory = self._repository.list_inventory()
        vehicles = self._repository.list_vehicles()
        energy = sum(
            (
                Decimal(str(item.daily_energy_kwh))
                for item in inventory
                if isinstance(item, EnergyConsumer)
            ),
            start=Decimal("0"),
        )
        return FleetSummary(
            inventory_count=len(inventory),
            vehicle_count=len(vehicles),
            thing_count=len(inventory) - len(vehicles),
            daily_energy_kwh=energy,
        )

    def beginner_vehicles(self) -> list[Vehicle]:
        return [
            vehicle
            for vehicle in self._repository.list_vehicles()
            if vehicle.is_suitable_for_beginner(self._beginner_threshold)
        ]

    def inventory(self) -> list[InventoryObject]:
        return list(self._repository.list_inventory())
