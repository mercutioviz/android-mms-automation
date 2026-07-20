"""
ADB communication layer.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ADB_PATH = Path(
    "/mnt/d/Android/platform-tools-latest-windows/platform-tools/adb.exe"
)


class AdbError(Exception):
    """Raised when ADB communication fails."""


class AdbClient:
    """Simple wrapper around Android Debug Bridge."""

    def __init__(self, adb_path: Path = ADB_PATH):
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
            raise AdbError(result.stderr)

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
