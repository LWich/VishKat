from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreateBase(BaseModel):
    inventory_number: str = Field(min_length=1, examples=["SC-001"])
    name: str = Field(min_length=1, examples=["Самокат у корпуса A"])


class VehicleCreateBase(InventoryCreateBase):
    beginner_ease: int = Field(ge=1, le=10)


class ScooterCreate(VehicleCreateBase):
    type: Literal["scooter"]
    daily_energy_kwh: Decimal = Field(ge=0)


class BicycleCreate(VehicleCreateBase):
    type: Literal["bicycle"]


class ElectricBicycleCreate(VehicleCreateBase):
    type: Literal["electric_bicycle"]
    daily_energy_kwh: Decimal = Field(ge=0)


VehicleCreate = Annotated[
    ScooterCreate | BicycleCreate | ElectricBicycleCreate,
    Field(discriminator="type"),
]


class HelmetCreate(InventoryCreateBase):
    type: Literal["helmet"]


class DockingStationCreate(InventoryCreateBase):
    type: Literal["docking_station"]
    daily_energy_kwh: Decimal = Field(ge=0)


class ChargingCabinetCreate(InventoryCreateBase):
    type: Literal["charging_cabinet"]
    daily_energy_kwh: Decimal = Field(ge=0)


ItemCreate = Annotated[
    HelmetCreate | DockingStationCreate | ChargingCabinetCreate,
    Field(discriminator="type"),
]


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str
    inventory_number: str
    name: str
    beginner_ease: int | None = None
    daily_energy_kwh: Decimal | None = None


class SummaryResponse(BaseModel):
    inventory_count: int
    vehicle_count: int
    thing_count: int
    daily_energy_kwh: Decimal


class ErrorResponse(BaseModel):
    detail: str
