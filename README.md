# genshin-map-download
download the whole map of genshin impact with this python code (for windows). by sardan_1024
needs python 3.12+
MAKE SURE THAT WHEN YOU INSTALLED PYTHON, YOU CHECKED THE BOX "add python.exe to PATH" if you didn't or not sure if you did, reinstall python.
# Genshin Map Downloader

This project is not affiliated with or endorsed by HoYoverse.
All game assets belong to their respective owners.
## Features
- Resume support (remembers where it was last time)
- Retry system

## Run
run this in powershell:
python -m pip install requests pillow tqdm
 then run "genshin_download_tiles.py"
 when download finishes, run "genshin_stitch.py"
if you find missing tiles in the downloaded map, delete the map (teyvat z15.png) NOT THE "tiles" folder or you will have to start again.
after you deleted the missing tiles map, run "MapManager.py" it will download missing tiles and restich them into a map.
