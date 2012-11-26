# -*- coding: utf8 -*-
import re
import os
from collections import Counter
import json

from config import Config

config = Config('config.json')


def calculate_popular(base_dir, lines):
    pn = r'\[IMAGE_VIEW\] image view (.+) at (\d+)'
    pn = re.compile(pn)
    counter = Counter()
    for line in lines:
        match = pn.search(line)
        if match.group(1).find(base_dir) != -1:
            path = os.path.relpath(match.group(1), base_dir)
        else:
            path = match.group(1)
        counter[path.replace('\\', '/')] += 1
    return dict(counter.most_common(50))


def run_calculate_popular():
    lines = [line.strip() for line in \
    file(config.image_view_log_file, 'r').readlines() if line.strip()]
    return calculate_popular(config.base_dir, lines)

if __name__ == "__main__":
    file(config.popular_result, 'w').write(json.dumps(run_calculate_popular()))
