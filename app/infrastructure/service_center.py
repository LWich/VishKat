from decimal import Decimal

from app.domain.interfaces import EnergyConsumer
from app.domain.models import Vehicle


class BasicServiceCenter:
    """Rejects energy-hungry devices; mechanical transport passes this check."""

    def __init__(self, max_daily_energy_kwh: Decimal) -> None:
        self._max_daily_energy_kwh = max_daily_energy_kwh

    def accepts(self, vehicle: Vehicle) -> bool:
        if not isinstance(vehicle, EnergyConsumer):
            return True
        return Decimal(str(vehicle.daily_energy_kwh)) <= self._max_daily_energy_kwh
