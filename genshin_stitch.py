from PIL import Image
import os

ZOOM = 15

# Your correct boundaries
MIN_X = -62
MAX_X = 63
MIN_Y = -56
MAX_Y = 58

TILE_SIZE = 256
TILES_FOLDER = f"tiles/z{ZOOM}"
OUTPUT_FILE = f"teyvat_z{ZOOM}.png"

width_tiles = MAX_X - MIN_X + 1
height_tiles = MAX_Y - MIN_Y + 1

canvas_width = width_tiles * TILE_SIZE
canvas_height = height_tiles * TILE_SIZE

print(f"Canvas size: {canvas_width} x {canvas_height}")
print(f"Tile grid: {width_tiles} x {height_tiles}")

canvas = Image.new("RGB", (canvas_width, canvas_height))

placed = 0
missing = 0

for x in range(MIN_X, MAX_X + 1):
    for y in range(MIN_Y, MAX_Y + 1):

        filename = f"{x}_{y}.jpg"  # <-- correct for your files
        filepath = os.path.join(TILES_FOLDER, filename)

        if os.path.exists(filepath):
            tile = Image.open(filepath)
            px = (x - MIN_X) * TILE_SIZE
            py = (MAX_Y - y) * TILE_SIZE  # flip Y so north is up
            canvas.paste(tile, (px, py))
            placed += 1
        else:
            missing += 1

print(f"Placed tiles: {placed}")
print(f"Missing tiles: {missing}")

print("Saving image... (this may take a while)")
canvas.save(OUTPUT_FILE, "PNG")
print("Done.")
