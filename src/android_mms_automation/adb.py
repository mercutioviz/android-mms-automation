"""
ADB communication layer.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from .config import load_settings

class AdbError(Exception):
    """Raised when ADB communication fails."""


class AdbClient:
    """Simple wrapper around Android Debug Bridge."""

    def __init__(self, adb_path: Path | None = None):
        if adb_path is None:
            settings = load_settings()
            adb_path = Path(settings.adb_path)

        self.adb_path = adb_path

    def run(self, *args: str) -> str:
        command = [
            str(self.adb_path),
            *args,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            message = result.stderr.strip() or "ADB command failed"
            raise AdbError(message)

        return result.stdout.strip()

    def shell(self, command: str) -> str:
        return self.run("shell", command)

    def devices(self) -> list[str]:
        output = self.run("devices")

        devices = []

        for line in output.splitlines():
            if "\tdevice" in line:
                serial = line.split("\t")[0]
                devices.append(serial)

        return devices
