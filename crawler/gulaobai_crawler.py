# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import requests
import sys
import os
import socket
from urllib import urlretrieve

sys.path.append(os.path.abspath('../'))
from config import Config

config = Config(os.path.abspath('../config.json'))

socket.setdefaulttimeout(10)



root = ''

total = 132


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0',
           'Accept-Encoding': 'gzip'}

def getlinks(url, selector, attr=False):
    response = requests.get(url, headers=headers)
    dom = pq(response.content)
    return [attr and elem.get(attr) or elem.text() for elem in dom(selector)]


def get_gallery_links(url):
    return getlinks(url, '#J_MonthPostsList_201211 .post-li a.post-meta', 'href')

def get_img_urls(container_page):
    return getlinks(container_page, '.photo_div>img', 'src')

def pull_imgs(srcs, filepath):
    for i in range(len(srcs)):
        try:
            filename = \
            os.path.join(filepath, str(i + 1) + os.path.splitext(srcs[i])[1])
            urlretrieve(srcs[i], filename)
            print 'save %s -> %s' % (srcs[i], filename)
        except:
            print 'error: %s' % (srcs[i])

if __name__ == '__main__':
    for gallery in get_gallery_links('http://gulaobai.diandian.com/archive'):
        print 'gallery: ', gallery
        curdir = os.path.join(config.base_dir, str(total))
        os.mkdir(curdir)
        total += 1
        results = get_img_urls(gallery)
        pull_imgs(results, curdir)
