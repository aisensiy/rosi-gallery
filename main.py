# -*- coding: utf8 -*-
from flask import Flask, send_file
import random
import time
import json
import os
import re

try:
    from PIL import Image
except:
    import Image

from config import Config
from cron import calculate_popular

config = Config('config.json')

app = Flask('rosi-view')
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
    folders = [file_name for file_name in os.listdir(config.base_dir) \
                if os.path.isdir(os.path.join(config.base_dir, file_name))]
    folders = map(lambda x: x.isdigit() and int(x) or x, folders)
    random.shuffle(folders)
    return json.dumps(folders)


@app.route("/list/<path:folder>")
def image_list(folder):
    filered = 'thumb'
    dir_path = os.path.join(config.base_dir, folder)
    if not os.path.isdir(dir_path):
        return "not found", 404
    images = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if re.search(image_pattern, file_name, re.IGNORECASE) \
            and re.search(filered, file_name, re.IGNORECASE) is None:
                images.append('/'.join([os.path.relpath(root, config.base_dir).replace('\\', '/'), file_name]))

    images.sort()
    sub_images = images[1:]
    random.shuffle(sub_images)
    return json.dumps([images[0]] + sub_images)


@app.route("/list/<folder>/<path:image>")
def get_image(folder, image):
    print folder, image
    file_path = os.path.join(config.base_dir, folder, image)
    if not os.path.isfile(file_path):
        return "not found", 404

    file_name, file_ext = os.path.splitext(file_path)
    log = file(config.image_view_log_file, 'a')
    log.write("[IMAGE_VIEW] image view %s at %d\n" % \
                                         (file_path.encode('utf8'), time.time()))
    return send_file(file_path, mimetype=content_type_map.get(file_ext.lower()))


@app.route("/list/<folder>/<path:image>/thumbnail")
def get_thumbnail(folder, image):
    file_path = os.path.join(config.base_dir, folder, image)
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
        if config.thumb_width < width:
            image.thumbnail((config.thumb_width, 1.0 * height / width * config.thumb_width), Image.ANTIALIAS)
            image.save(thumb_path)
        else:
            return send_file(file_path, mimetype=content_type_map.get(file_ext.lower()))
    return send_file(thumb_path, mimetype=content_type_map.get(file_ext.lower()))


@app.route("/popular")
def get_popular():
    lines = [line.strip() for line in \
    file(config.image_view_log_file, 'r').readlines() if line.strip()]
    populars = calculate_popular(config.base_dir, lines)
    return json.dumps(populars.keys())


if __name__ == "__main__":
    app.run(debug=True)
