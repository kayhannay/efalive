#!/usr/bin/env python3
"""Compile .po translation files into .mo files."""

import glob
import os
import subprocess
import sys

PACKAGES = ["efaLiveTools", "autobackup"]
OUTPUT_DIR = "locale"


def compile_translations():
    print(f"Building locales in: {os.getcwd()}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for package in PACKAGES:
        po_dir = os.path.join("i18n", package, "po_files")
        for po in glob.glob(os.path.join(po_dir, "*.po")):
            lang = os.path.splitext(os.path.basename(po))[0]
            mo_dir = os.path.join(OUTPUT_DIR, lang, "LC_MESSAGES")
            os.makedirs(mo_dir, exist_ok=True)
            mo = os.path.join(mo_dir, f"{package}.mo")

            po_mtime = os.path.getmtime(po)
            if os.path.exists(mo) and os.path.getmtime(mo) >= po_mtime:
                print(f"  {mo} is up to date")
                continue

            print(f"  {po} -> {mo}")
            subprocess.check_call(["msgfmt", "-o", mo, po])

    print("Done.")


if __name__ == "__main__":
    compile_translations()
