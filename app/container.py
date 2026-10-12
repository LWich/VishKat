from dependency_injector import containers, providers

from app.application.services import FleetService
from app.core.config import Settings
from app.infrastructure.repositories import InMemoryFleetRepository
from app.infrastructure.service_center import BasicServiceCenter


class Container(containers.DeclarativeContainer):
    """Composition root: all concrete dependencies are selected here."""

    settings = providers.Singleton(Settings)
    repository = providers.Singleton(InMemoryFleetRepository)
    service_center = providers.Singleton(
        BasicServiceCenter,
        max_daily_energy_kwh=settings.provided.max_device_daily_energy_kwh,
    )
    fleet_service = providers.Singleton(
        FleetService,
        repository=repository,
        service_center=service_center,
        beginner_threshold=settings.provided.beginner_threshold,
    )
