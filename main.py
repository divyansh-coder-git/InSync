from pathlib import Path
from flask import Flask, jsonify, send_from_directory
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Visit /manifest to see the list of files</h1>"

path = r"C:\Users\My Songs" # Change this path to your music folder to watch in your computer
folder = Path(path)
def get_manifest():
    files = []
    for f in folder.iterdir():
        if f.is_file():
            if f.suffix.lower() in [".mp3", ".m4a"]:
                info = f.stat()
                if time.time() - info.st_mtime >= 10:
                    files.append({"name": f.name, "size": info.st_size, "mtime": info.st_mtime})
    return files

@app.route("/manifest")
def send_manifest():
    return jsonify(get_manifest())

@app.route("/files/<name>")
def get_file(name):
    return send_from_directory(folder, name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)