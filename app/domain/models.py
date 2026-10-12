from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar

from app.domain.exceptions import InvalidEntityError


@dataclass(frozen=True, slots=True, kw_only=True)
class InventoryObject:
    """Base class for anything placed on the balance sheet."""

    kind: ClassVar[str] = "inventory_object"
    inventory_number: str
    name: str

    def __post_init__(self) -> None:
        if not self.inventory_number.strip():
            raise InvalidEntityError("Inventory number must not be blank")
        if not self.name.strip():
            raise InvalidEntityError("Name must not be blank")


@dataclass(frozen=True, slots=True, kw_only=True)
class Vehicle(InventoryObject):
    """Base class for rental transport."""

    kind: ClassVar[str] = "vehicle"
    beginner_ease: int

    def __post_init__(self) -> None:
        super(Vehicle, self).__post_init__()
        if not 1 <= self.beginner_ease <= 10:
            raise InvalidEntityError("Beginner ease must be between 1 and 10")

    def is_suitable_for_beginner(self, threshold: int) -> bool:
        return self.beginner_ease >= threshold


def _validate_energy(value: Decimal) -> None:
    if value < 0:
        raise InvalidEntityError("Daily energy consumption must not be negative")


@dataclass(frozen=True, slots=True, kw_only=True)
class Scooter(Vehicle):
    kind: ClassVar[str] = "scooter"
    daily_energy_kwh: Decimal

    def __post_init__(self) -> None:
        Vehicle.__post_init__(self)
        _validate_energy(self.daily_energy_kwh)


@dataclass(frozen=True, slots=True, kw_only=True)
class Bicycle(Vehicle):
    kind: ClassVar[str] = "bicycle"


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectricBicycle(Vehicle):
    kind: ClassVar[str] = "electric_bicycle"
    daily_energy_kwh: Decimal

    def __post_init__(self) -> None:
        Vehicle.__post_init__(self)
        _validate_energy(self.daily_energy_kwh)


@dataclass(frozen=True, slots=True, kw_only=True)
class Helmet(InventoryObject):
    kind: ClassVar[str] = "helmet"


@dataclass(frozen=True, slots=True, kw_only=True)
class DockingStation(InventoryObject):
    kind: ClassVar[str] = "docking_station"
    daily_energy_kwh: Decimal

    def __post_init__(self) -> None:
        InventoryObject.__post_init__(self)
        _validate_energy(self.daily_energy_kwh)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChargingCabinet(InventoryObject):
    kind: ClassVar[str] = "charging_cabinet"
    daily_energy_kwh: Decimal

    def __post_init__(self) -> None:
        InventoryObject.__post_init__(self)
        _validate_energy(self.daily_energy_kwh)
