"""
Android device abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass

from .adb import AdbClient


@dataclass
class DeviceInfo:
    serial: str
    model: str
    android_version: str
    resolution: str
    density: str


class AndroidDevice:
    """
    Represents a connected Android device.
    """

    def __init__(
        self,
        adb: AdbClient | None = None,
        serial: str | None = None,
    ):
        self.adb = adb or AdbClient()

        devices = self.adb.devices()

        if not devices:
            raise RuntimeError("No Android devices connected")

        self.serial = serial or devices[0]

    def shell(self, command: str) -> str:
        return self.adb.shell(command)

    @property
    def model(self) -> str:
        return self.shell(
            "getprop ro.product.model"
        )

    @property
    def android_version(self) -> str:
        return self.shell(
            "getprop ro.build.version.release"
        )

    @property
    def resolution(self) -> str:
        output = self.shell("wm size")

        return output.replace(
            "Physical size: ",
            ""
        )

    @property
    def density(self) -> str:
        output = self.shell("wm density")

        return output.replace(
            "Physical density: ",
            ""
        )

    def info(self) -> DeviceInfo:
        return DeviceInfo(
            serial=self.serial,
            model=self.model,
            android_version=self.android_version,
            resolution=self.resolution,
            density=self.density,
        )
