#!/usr/bin/env python3
"""
pack_theme_assets.py - Tool to package an Emoji/Animation Theme into a standalone assets.bin partition

Usage:
    # 1. Package and flash DB-Robot theme:
    python scripts/pack_theme_assets.py --theme dbrobot --flash --port COM5

    # 2. Package and flash Otto theme:
    python scripts/pack_theme_assets.py --theme otto --flash --port COM5

    # 3. Package custom theme folder:
    python scripts/pack_theme_assets.py --theme_dir /path/to/gifs --output build/assets_custom.bin
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

DEFAULT_OFFSET = "0x800000"  # Standard assets partition offset in 16MB partition table

def main():
    parser = argparse.ArgumentParser(description="Package Emoji Theme into standalone assets.bin partition")
    parser.add_argument("--theme", default="dbrobot", choices=["dbrobot", "otto"], help="Preset theme to package (default: dbrobot)")
    parser.add_argument("--theme_dir", default=None, help="Custom directory containing emoji GIFs or PNGs")
    parser.add_argument("--output", default=None, help="Output path for the assets binary")
    parser.add_argument("--sdkconfig", default="sdkconfig", help="Path to sdkconfig (default: sdkconfig)")
    parser.add_argument("--flash", action="store_true", help="Automatically flash to ESP32 device after packaging")
    parser.add_argument("--port", default=None, help="Serial port for flashing (e.g., COM5 or /dev/ttyUSB0)")
    parser.add_argument("--baud", default="460800", help="Baud rate for flashing (default: 460800)")
    parser.add_argument("--chip", default="esp32s3", help="Target chip (default: esp32s3)")

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    theme_name = args.theme
    theme_dir = args.theme_dir
    output_bin = args.output

    if theme_dir:
        theme_arg = os.path.abspath(theme_dir)
        if not output_bin:
            output_bin = "build/assets_custom.bin"
    elif theme_name == "dbrobot":
        theme_arg = "dbrobot"
        if not output_bin:
            output_bin = "build/assets_dbrobot.bin"
    elif theme_name == "otto":
        theme_arg = "otto-gif"
        if not output_bin:
            output_bin = "build/assets_otto.bin"
    else:
        theme_arg = theme_name
        if not output_bin:
            output_bin = f"build/assets_{theme_name}.bin"

    print("=" * 60)
    print(" XiaoZhi AI - Emoji Theme Asset Packager (Huong A)")
    print("=" * 60)
    print(f" Theme Selected         : {theme_name}")
    print(f" Theme Identifier/Dir   : {theme_arg}")
    print(f" Target Output Binary   : {output_bin}")
    print(f" Flash Partition Offset : {DEFAULT_OFFSET} (assets partition)")
    print("-" * 60)

    # Use scripts/build_default_assets.py
    cmd = [
        sys.executable,
        os.path.join("scripts", "build_default_assets.py"),
        "--sdkconfig", args.sdkconfig,
        "--emoji_collection", theme_arg,
        "--output", output_bin
    ]

    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"Error: Asset packaging failed with exit code {res.returncode}")
        sys.exit(res.returncode)

    if not os.path.exists(output_bin):
        print(f"Error: Output binary not found: {output_bin}")
        sys.exit(1)

    size_bytes = os.path.getsize(output_bin)
    print("-" * 60)
    print(f"[SUCCESS] Package created: {output_bin} ({size_bytes / 1024:.2f} KB)")
    print("This binary can be flashed independently without rebuilding or touching xiaozhi.bin!")
    print(f"Flash command:")
    port_arg = f"-p {args.port} " if args.port else ""
    flash_cmd = f"python -m esptool --chip {args.chip} {port_arg}-b {args.baud} write_flash {DEFAULT_OFFSET} {output_bin}"
    print(f"  {flash_cmd}")
    print("=" * 60)

    if args.flash:
        print(f"Flashing to device at {DEFAULT_OFFSET} via {args.port or 'default port'}...")
        cmd_flash = [
            sys.executable, "-m", "esptool",
            "--chip", args.chip,
            "-b", args.baud,
            "write_flash", DEFAULT_OFFSET, output_bin
        ]
        if args.port:
            cmd_flash.insert(4, "-p")
            cmd_flash.insert(5, args.port)
        flash_res = subprocess.run(cmd_flash)
        if flash_res.returncode != 0:
            print(f"Flash failed with code {flash_res.returncode}")
            sys.exit(flash_res.returncode)
        print("[SUCCESS] Theme flashed to assets partition successfully!")

if __name__ == "__main__":
    main()
