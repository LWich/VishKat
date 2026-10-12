from app.domain.exceptions import DuplicateInventoryNumberError
from app.domain.models import InventoryObject, Vehicle


class InMemoryFleetRepository:
    """Process-local storage suitable for the assignment and unit tests."""

    def __init__(self) -> None:
        self._items: dict[str, InventoryObject] = {}

    def add(self, item: InventoryObject) -> None:
        if item.inventory_number in self._items:
            raise DuplicateInventoryNumberError(
                f"Inventory number {item.inventory_number!r} already exists"
            )
        self._items[item.inventory_number] = item

    def list_inventory(self) -> list[InventoryObject]:
        return list(self._items.values())

    def list_vehicles(self) -> list[Vehicle]:
        return [item for item in self._items.values() if isinstance(item, Vehicle)]
