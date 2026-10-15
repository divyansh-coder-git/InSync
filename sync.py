#This file is to be run in mobile device, use Termux with python installed and storage permissions given
from pathlib import Path
import requests
from urllib.parse import quote
import time
from datetime import datetime

SERVER = "http://192.168.78.136:8000" #Enter the server IP(which flask hosts on the local network)
LOCAL = Path.home() / "storage" / "shared" / "Music" # Enter your music folder to watch in mobile
def sync_once():
    LOCAL.mkdir(parents=True, exist_ok=True)

    remote = requests.get(f"{SERVER}/manifest", timeout=10).json()
    remote_sizes = {item["name"] : item["size"] for item in remote}

    local_names = {f.name for f in LOCAL.iterdir() if f.is_file()}
    local_sizes = {f.name:f.stat().st_size for f in LOCAL.iterdir() if f.is_file()}

    to_download = []
    for name, size in remote_sizes.items():
        if size != local_sizes.get(name):
            to_download.append(name)
    
    print(f"{len(to_download)} songs to download")
    for name in sorted(to_download):
        print(name)

    for name in sorted(to_download):
        url = f"{SERVER}/files/{quote(name)}"
        final_path = LOCAL / name
        part_path = LOCAL / (name + ".part")
        try:
            with requests.get(url, stream=True, timeout=10) as r:
                r.raise_for_status()
                with open(part_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 256):
                        f.write(chunk)
            part_path.replace(final_path)
            print("downloaded:", name)
        except requests.RequestException as e:
            print("failed:", name, e)

    print("----------------------------------------------------")
    print("Completed one sync at: ", datetime.now())
    print("----------------------------------------------------")
while True:
    try:
        sync_once()
    except Exception as e:
        print("Error occured while sync: ", e)
    time.sleep(30)