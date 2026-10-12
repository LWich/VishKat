from decimal import Decimal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="VYSHKAT_",
        extra="ignore",
    )

    app_name: str = "VyshKat API"
    api_prefix: str = "/api/v1"
    beginner_threshold: int = Field(default=6, ge=1, le=10)
    max_device_daily_energy_kwh: Decimal = Field(default=Decimal("25"), gt=0)
