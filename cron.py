# -*- coding: utf8 -*-
import re
import os
from collections import Counter
import json

popular_result = "popular.txt"


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
    base_dir = 'e:\\rosi'
    image_view_log_file = 'image_view.log'
    lines = [line.strip() for line in \
    file(image_view_log_file, 'r').readlines() if line.strip()]
    return calculate_popular(base_dir, lines)

if __name__ == "__main__":
    file(popular_result, 'w').write(json.dumps(run_calculate_popular()))
