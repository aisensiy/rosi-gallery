from flask import Flask, send_file
import json
import os

app = Flask('rosi-view')
base_dir = "e:\\rosi"

content_type_map = {
    'jpeg': 'image/jpeg',
    'jpg':  'image/jpeg',
    'png':  'image/png',
    'gif':  'image/gif'
}


@app.route("/")
def index():
    return file("index.html").read()


@app.route("/list")
def folder_list():
    folders = [file_name for file_name in os.listdir(base_dir) \
                if os.path.isdir(os.path.join(base_dir, file_name))]
    folders = map(lambda x: x.isdigit() and int(x) or x, folders)
    folders.sort()
    return json.dumps(folders)


@app.route("/list/<folder>")
def image_list(folder):
    dir_path = os.path.join(base_dir, folder)
    if not os.path.isdir(dir_path):
        return "not found", 404
    images = ['/'.join([folder, file_name]) for file_name in os.listdir(dir_path) \
                if os.path.isfile(os.path.join(dir_path, file_name))]
    images.sort()
    return json.dumps(images)


@app.route("/list/<folder>/<image>")
def get_image(folder, image):
    file_path = os.path.join(base_dir, folder, image)
    if not os.path.isfile(file_path):
        return "not found", 404

    file_name, file_ext = os.path.splitext(file_path)
    return send_file(file_path, mimetype=content_type_map.get(file_ext.lower()))

if __name__ == "__main__":
    app.run(debug=True)
