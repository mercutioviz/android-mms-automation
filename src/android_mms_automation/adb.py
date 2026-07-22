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
        self.settings = load_settings()

        if adb_path is None:
            adb_path = Path(self.settings.adb_path)

        self.adb_path = adb_path

    def run(self, *args: str) -> str:
        command = [str(self.adb_path)]

        if self.settings.device_serial:
            command.extend(["-s", self.settings.device_serial])

        command.extend(args)

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

    def exec_out(self, *args: str) -> bytes:
        command = [str(self.adb_path)]

        if self.settings.device_serial:
            command.extend(["-s", self.settings.device_serial])

        command.append("exec-out")
        command.extend(args)

        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            message = result.stderr.decode(errors="replace").strip()
            raise AdbError(message or "ADB exec-out failed")

        return result.stdout
 

