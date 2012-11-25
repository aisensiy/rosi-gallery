# -*- coding: utf8 -*-
from flask import Flask, send_file
from PIL import Image
import time
import json
import os
import re

app = Flask('rosi-view')
base_dir = "e:\\rosi"
thumb_width = 300
image_view_log_file = 'image_view.log'
image_pattern = r'\.(gif|png|jpeg|jpg)$'

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


@app.route("/list/<path:folder>")
def image_list(folder):
    filered = 'thumb'
    dir_path = os.path.join(base_dir, folder)
    if not os.path.isdir(dir_path):
        return "not found", 404
    images = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if re.search(image_pattern, file_name, re.IGNORECASE) \
            and re.search(filered, file_name, re.IGNORECASE) is None:
                images.append('/'.join([os.path.relpath(root, base_dir).replace('\\', '/'), file_name]))

    images.sort()
    return json.dumps(images)


@app.route("/list/<folder>/<path:image>")
def get_image(folder, image):
    print folder, image
    file_path = os.path.join(base_dir, folder, image)
    if not os.path.isfile(file_path):
        return "not found", 404

    file_name, file_ext = os.path.splitext(file_path)
    file(image_view_log_file, 'a').write("[IMAGE_VIEW] image view %s at %d\n" % \
                                         (('/'.join([folder, image])).encode('utf8'), time.time()))
    return send_file(file_path, mimetype=content_type_map.get(file_ext.lower()))


@app.route("/list/<folder>/<path:image>/thumbnail")
def get_thumbnail(folder, image):
    file_path = os.path.join(base_dir, folder, image)
    if not os.path.isfile(file_path):
        return "not found", 404

    file_name, file_ext = os.path.splitext(file_path)
    file_ext = file_ext[1:]
    thumb_path = file_name + '.thumb.' + file_ext
    if not os.path.isfile(thumb_path):
        print 'read: ', file_path, ' thumbnail'
        image = Image.open(file_path)
        width, height = image.size
        print width, height
        print file_ext
        if thumb_width < width:
            image.thumbnail((thumb_width, 1.0 * height / width * thumb_width), Image.ANTIALIAS)
            image.save(thumb_path)
        else:
            return send_file(file_path, mimetype=content_type_map.get(file_ext.lower()))
    return send_file(thumb_path, mimetype=content_type_map.get(file_ext.lower()))


if __name__ == "__main__":
    app.run(debug=True)
