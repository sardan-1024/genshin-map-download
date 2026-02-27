import os
import re
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

# ================= CONFIG =================

ZOOM = 15
BASE_URL = "https://game-cdn.appsample.com/gim/map-teyvat"
VERSION = None  # None = auto detect (recommended)
SAVE_DIR = Path(f"tiles/z{ZOOM}")
THREADS = 16
TILE_SIZE = 256
EXPAND_RINGS = 1  # how many edge expansions

# ==========================================


# ---------- Version Auto Detect ----------

def detect_latest_version():
    print("Detecting latest map version...")
    for i in range(100, 40, -1):
        test = f"v{i}-rc1"
        url = f"{BASE_URL}/{test}/{ZOOM}/tile-0_0.jpg"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print("Using version:", test)
                return test
        except:
            pass
    raise Exception("Could not detect version")


if VERSION is None:
    VERSION = detect_latest_version()

TILE_URL = f"{BASE_URL}/{VERSION}/{ZOOM}/tile-{{x}}_{{y}}.jpg"

SAVE_DIR.mkdir(parents=True, exist_ok=True)

pattern = re.compile(r"(-?\d+)_(-?\d+)\.jpg")


# ---------- Load existing tiles ----------

def load_existing():
    xs, ys = [], []
    for file in SAVE_DIR.glob("*.jpg"):
        match = pattern.match(file.name)
        if match:
            x, y = map(int, match.groups())
            xs.append(x)
            ys.append(y)
    if not xs:
        return None
    return min(xs), max(xs), min(ys), max(ys)


# ---------- Download tile ----------

def download_tile(x, y):
    filepath = SAVE_DIR / f"{x}_{y}.jpg"
    if filepath.exists():
        return

    url = TILE_URL.format(x=x, y=y)

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and len(r.content) > 1000:
            filepath.write_bytes(r.content)
            print(f"Downloaded {x}_{y}")
    except:
        pass


# ---------- Detect missing tiles ----------

def find_missing(min_x, max_x, min_y, max_y):
    missing = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if not (SAVE_DIR / f"{x}_{y}.jpg").exists():
                missing.append((x, y))
    return missing


# ---------- Expand edges ----------

def expand_edges(min_x, max_x, min_y, max_y, rings):
    targets = []

    for r in range(1, rings + 1):
        for x in range(min_x - r, max_x + r + 1):
            targets.append((x, min_y - r))
            targets.append((x, max_y + r))

        for y in range(min_y - r + 1, max_y + r):
            targets.append((min_x - r, y))
            targets.append((max_x + r, y))

    return targets


# ---------- Stitch ----------

def stitch():
    bounds = load_existing()
    if not bounds:
        print("No tiles to stitch.")
        return

    min_x, max_x, min_y, max_y = bounds

    width = (max_x - min_x + 1) * TILE_SIZE
    height = (max_y - min_y + 1) * TILE_SIZE

    print(f"Stitching canvas: {width} x {height}")

    canvas = Image.new("RGB", (width, height))

    for file in SAVE_DIR.glob("*.jpg"):
        match = pattern.match(file.name)
        if not match:
            continue
        x, y = map(int, match.groups())
        img = Image.open(file)
        px = (x - min_x) * TILE_SIZE
        py = (max_y - y) * TILE_SIZE
        canvas.paste(img, (px, py))

    canvas.save(f"teyvat_z{ZOOM}.png")
    print("Stitch complete.")


# ================= RUN =================

bounds = load_existing()

if bounds:
    min_x, max_x, min_y, max_y = bounds
    print("Current bounds:", bounds)

    # 1. Fix missing inside area
    missing = find_missing(min_x, max_x, min_y, max_y)
    print("Missing tiles:", len(missing))

    with ThreadPoolExecutor(max_workers=THREADS) as exe:
        exe.map(lambda t: download_tile(*t), missing)

    # 2. Expand edges
    edge_targets = expand_edges(min_x, max_x, min_y, max_y, EXPAND_RINGS)

    with ThreadPoolExecutor(max_workers=THREADS) as exe:
        exe.map(lambda t: download_tile(*t), edge_targets)

else:
    print("No tiles found. Run initial full downloader first.")

# 3. Stitch
stitch()
