from typing import cast

from fastapi import Request

from app.application.services import FleetService


def get_fleet_service(request: Request) -> FleetService:
    return cast(FleetService, request.app.state.container.fleet_service())
