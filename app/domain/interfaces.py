from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from app.domain.models import InventoryObject, Vehicle


@runtime_checkable
class EnergyConsumer(Protocol):
    """A device whose daily energy consumption can be reported."""

    @property
    def daily_energy_kwh(self) -> object: ...


@runtime_checkable
class Inventoriable(Protocol):
    """An object tracked by a unique inventory number."""

    @property
    def inventory_number(self) -> str: ...

    @property
    def name(self) -> str: ...


class ServiceCenter(Protocol):
    """Port for mandatory vehicle inspection."""

    def accepts(self, vehicle: Vehicle) -> bool: ...


class FleetRepository(Protocol):
    """Storage port used by the application service."""

    def add(self, item: InventoryObject) -> None: ...

    def list_inventory(self) -> Sequence[InventoryObject]: ...

    def list_vehicles(self) -> Sequence[Vehicle]: ...
