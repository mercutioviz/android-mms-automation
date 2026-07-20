"""
Command-line interface.
"""

from __future__ import annotations

import typer

from .device import AndroidDevice


app = typer.Typer(
    name="android-mms",
    help="Android MMS Automation Framework",
    no_args_is_help=True,
)

@app.callback()
def main():
    """
    Android MMS Automation Framework.
    """
    pass

@app.command()
def device_info():
    """
    Display connected Android device information.
    """

    device = AndroidDevice()

    info = device.info()

    print()
    print("Android Device")
    print("==============")
    print(f"Serial:          {info.serial}")
    print(f"Model:           {info.model}")
    print(f"Android:         {info.android_version}")
    print(f"Resolution:      {info.resolution}")
    print(f"Density:         {info.density}")
    print()


if __name__ == "__main__":
    app()
