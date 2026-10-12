from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_fleet_service
from app.api.mappers import to_item, to_response, to_vehicle
from app.api.schemas import InventoryResponse, ItemCreate, SummaryResponse, VehicleCreate
from app.application.services import FleetService

router = APIRouter()
FleetServiceDependency = Annotated[FleetService, Depends(get_fleet_service)]


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/vehicles",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["fleet"],
)
def add_vehicle(payload: VehicleCreate, service: FleetServiceDependency) -> InventoryResponse:
    return to_response(service.add_vehicle(to_vehicle(payload)))


@router.post(
    "/items",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["fleet"],
)
def add_item(payload: ItemCreate, service: FleetServiceDependency) -> InventoryResponse:
    return to_response(service.add_item(to_item(payload)))


@router.get("/reports/summary", response_model=SummaryResponse, tags=["reports"])
def summary(service: FleetServiceDependency) -> SummaryResponse:
    return SummaryResponse.model_validate(service.summary(), from_attributes=True)


@router.get(
    "/vehicles/beginner",
    response_model=list[InventoryResponse],
    tags=["reports"],
)
def beginner_vehicles(service: FleetServiceDependency) -> list[InventoryResponse]:
    return [to_response(vehicle) for vehicle in service.beginner_vehicles()]


@router.get("/inventory", response_model=list[InventoryResponse], tags=["reports"])
def inventory(service: FleetServiceDependency) -> list[InventoryResponse]:
    return [to_response(item) for item in service.inventory()]
