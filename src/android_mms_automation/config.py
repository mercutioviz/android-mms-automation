from pathlib import Path
import tomllib

from pydantic import BaseModel


class Settings(BaseModel):
    adb_path: str
    device_serial: str | None = None


def load_settings(
    path: Path = Path("config/settings.toml"),
) -> Settings:
    """Load project settings from a TOML file."""

    with path.open("rb") as f:
        data = tomllib.load(f)

    return Settings(**data)
