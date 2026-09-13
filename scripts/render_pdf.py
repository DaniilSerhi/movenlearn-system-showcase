"""Render the local HTML using an isolated Chrome profile; no font downloads."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def chrome_binary(explicit=None):
    if explicit:
        return explicit
    for name in ("chrome-headless-shell", "google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    for cache in (Path.home() / "Library" / "Caches" / "ms-playwright",
                  Path.home() / ".cache" / "ms-playwright"):
        candidates = sorted(cache.glob("chromium_headless_shell-*/**/chrome-headless-shell"))
        if candidates:
            return str(candidates[-1])
    mac = Path(os.sep) / "Applications" / "Google Chrome.app" / "Contents" / "MacOS" / "Google Chrome"
    if mac.is_file():
        return str(mac)
    raise SystemExit("Chrome/Chromium not found. Supply --chrome with its executable.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome")
    args = parser.parse_args()
    for tool in ("pdfinfo", "pdftotext", "pdftoppm", "pdffonts"):
        if not shutil.which(tool):
            raise SystemExit("Install Poppler: missing " + tool)
    with tempfile.TemporaryDirectory(prefix="showcase-chrome-") as profile:
        cmd = [chrome_binary(args.chrome), "--headless", "--disable-gpu", "--disable-background-networking",
               "--disable-extensions", "--no-first-run", "--no-default-browser-check",
               "--no-pdf-header-footer", "--user-data-dir=" + profile, "--timeout=20000",
               "--virtual-time-budget=3000", "--print-to-pdf=" + str(ROOT / "demo/pdf/sample.pdf"),
               (ROOT / "demo/pdf/sample.html").as_uri()]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
        except subprocess.TimeoutExpired:
            raise SystemExit("Chrome did not exit. Try a headless-shell executable with --chrome.")
        if result.returncode:
            raise SystemExit("Chrome rendering failed; check local sandbox permissions and executable.")
    subprocess.run([sys.executable, str(ROOT / "scripts/verify_pdf.py")], check=True)
    subprocess.run(["pdftoppm", "-singlefile", "-png", "-r", "120",
                    str(ROOT / "demo/pdf/sample.pdf"), str(ROOT / "demo/pdf/preview")], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print("Rendered demo/pdf/sample.pdf and preview.png; inspect the image before acceptance.")


if __name__ == "__main__":
    main()

