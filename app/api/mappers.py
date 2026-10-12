from app.api.schemas import (
    BicycleCreate,
    ChargingCabinetCreate,
    DockingStationCreate,
    ElectricBicycleCreate,
    HelmetCreate,
    InventoryResponse,
    ItemCreate,
    ScooterCreate,
    VehicleCreate,
)
from app.domain.models import (
    Bicycle,
    ChargingCabinet,
    DockingStation,
    ElectricBicycle,
    Helmet,
    InventoryObject,
    Scooter,
    Vehicle,
)


def to_vehicle(payload: VehicleCreate) -> Vehicle:
    if isinstance(payload, ScooterCreate):
        return Scooter(
            inventory_number=payload.inventory_number,
            name=payload.name,
            beginner_ease=payload.beginner_ease,
            daily_energy_kwh=payload.daily_energy_kwh,
        )
    if isinstance(payload, ElectricBicycleCreate):
        return ElectricBicycle(
            inventory_number=payload.inventory_number,
            name=payload.name,
            beginner_ease=payload.beginner_ease,
            daily_energy_kwh=payload.daily_energy_kwh,
        )
    if isinstance(payload, BicycleCreate):
        return Bicycle(
            inventory_number=payload.inventory_number,
            name=payload.name,
            beginner_ease=payload.beginner_ease,
        )
    raise TypeError(f"Unsupported vehicle payload: {type(payload)!r}")


def to_item(payload: ItemCreate) -> InventoryObject:
    common = {"inventory_number": payload.inventory_number, "name": payload.name}
    if isinstance(payload, HelmetCreate):
        return Helmet(**common)
    if isinstance(payload, DockingStationCreate):
        return DockingStation(**common, daily_energy_kwh=payload.daily_energy_kwh)
    if isinstance(payload, ChargingCabinetCreate):
        return ChargingCabinet(**common, daily_energy_kwh=payload.daily_energy_kwh)
    raise TypeError(f"Unsupported item payload: {type(payload)!r}")


def to_response(item: InventoryObject) -> InventoryResponse:
    return InventoryResponse(
        type=item.kind,
        inventory_number=item.inventory_number,
        name=item.name,
        beginner_ease=getattr(item, "beginner_ease", None),
        daily_energy_kwh=getattr(item, "daily_energy_kwh", None),
    )
