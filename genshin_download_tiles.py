import os
import requests
from time import sleep

ZOOM = 15
MIN_X = -62
MAX_X = 63
MIN_Y = -56
MAX_Y = 58

BASE_URL = f"https://game-cdn.appsample.com/gim/map-teyvat/v63-rc1/{ZOOM}"
SAVE_DIR = f"tiles/z{ZOOM}"

os.makedirs(SAVE_DIR, exist_ok=True)

total = (MAX_X - MIN_X + 1) * (MAX_Y - MIN_Y + 1)
count = 0

print(f"Downloading zoom {ZOOM}")
print(f"Range X:{MIN_X}→{MAX_X}  Y:{MIN_Y}→{MAX_Y}")
print(f"Total tiles: {total}")
print("Resume safe. Ctrl+C anytime.\n")

for y in range(MAX_Y, MIN_Y - 1, -1):
    for x in range(MIN_X, MAX_X + 1):

        filename = f"{x}_{y}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)

        count += 1

        if os.path.exists(filepath):
            continue

        url = f"{BASE_URL}/tile-{x}_{y}.jpg"

        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(r.content)
                print(f"[{count}/{total}] OK   {x},{y}")
            else:
                print(f"[{count}/{total}] 404  {x},{y}")

            sleep(0.05)

        except Exception as e:
            print(f"[{count}/{total}] FAIL {x},{y}")

print("\nDownload complete.")
