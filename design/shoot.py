"""Capture stills of the local site with headless Chrome (verification step).

    python design/shoot.py <outdir> <name>=<path>@<width>x<height> ...

The site must be served at http://localhost:8000. Paths may carry ?seek=scene:progress
(see assets/motion.js) to freeze a motion scene at an exact progress value.
"""
import subprocess
import sys
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# Isolated throwaway profile: never touches the user's own Chrome session.
import tempfile, os, shutil
PROFILE = os.path.join(tempfile.gettempdir(), "obscur4-shoot-profile")


def shoot(out, name, path, w, h):
    target = (out / f"{name}.png").resolve()
    profile = tempfile.mkdtemp(prefix="obscur4-shoot-")
    subprocess.run([
        CHROME, "--headless=new", f"--user-data-dir={profile}", "--no-first-run", "--no-default-browser-check",
        "--disable-gpu", "--hide-scrollbars", 
        f"--window-size={w},{h}", f"--screenshot={target}",
        f"http://localhost:8000{path}",
    ], check=True, capture_output=True, timeout=90)
    shutil.rmtree(profile, ignore_errors=True)
    return target


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for spec in sys.argv[2:]:
        name, rest = spec.split("=", 1)
        path, size = rest.rsplit("@", 1)
        w, h = (int(x) for x in size.split("x"))
        print(shoot(out, name, path, w, h))


if __name__ == "__main__":
    main()
