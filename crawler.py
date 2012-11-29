# -*- coding: utf8 -*-
from BeautifulSoup import BeautifulSoup as Soup
import urllib2
import re
import time
from StringIO import StringIO
import gzip
import socket
import os
import pprint
from urllib import urlretrieve
from soupselector import select
from config import Config

socket.setdefaulttimeout(10)

config = Config('config.json')
total = config.total + 1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0',
           'Accept-Encoding': 'gzip'}
log = 'log.txt'


def nomalize_url(url):
    """
    normalize url:
    to lower case | no hash | has slash if there is only domain url
    """
    url = url.lower()
    url = re.sub(r'#[^/]*$', '', url)
    url = re.sub(r'^(\w+://([0-9a-z\-]+\.)+[0-9a-z\-]+)/?$', r'\1/', url)
    return url


def get_page_links(url):
    soup = Soup(load_page(url))
    print 'open %s %s' % (soup.title.string.encode('utf-8'), url)
    links = select(soup, 'a.post-article')
    #links = soup.findAll('a', href=re.compile(r'^http://duoduovision.diandian.com/post/\d{4}-\d{2}-\d{2}/'))
    #return list(set([nomalize_url(a['href']) for a in links]))
    return [nomalize_url(a['href']) for a in links]


def get_img_links(url):
    soup = Soup(load_page(url))
    imgs = select(soup, 'a.post-meidaurl img')
    return [img['src'] for img in imgs]


def load_page(url):
    "获取单独页面"
    print url
    req = urllib2.Request(url, None, headers)
    body = ''
    try:
        resp = urllib2.urlopen(req)
        body = resp.read()
        if resp.headers.get('content-encoding', '') == 'gzip':
            body = gzip.GzipFile(fileobj=StringIO(body)).read()
    except:
        pass
    return body

#def get_img_src(soup):
#    src = soup.findAll('img', src=re.compile(r'^http://www.rosimi.com/attach/\d{4}-\d{2}-\d{2}/'))[0]
#    return src['src']

#def down_img(src, filename):
#    imgData = load_page(src)
#    output = open(filename, 'wb');
#    output.write(imgData);


def pull_imgs(srcs, filepath):
    for i in range(len(srcs)):
        try:
            filename = \
            os.path.join(filepath, str(i + 1) + os.path.splitext(srcs[i])[1])
            urlretrieve(srcs[i], filename)
            print 'save %s -> %s' % (srcs[i], filename)
        except:
            print 'error: %s' % (srcs[i])


def fronter(url):
    global total
    rosis = get_page_links(url)
    for rosi in rosis:
        curdir = os.path.join(config.base_dir, str(total))
        os.mkdir(curdir)
        total += 1
        pull_imgs(get_img_links(rosi), curdir)
        print 'load all page in ' + rosi


if __name__ == '__main__':
    #pprint.pprint(get_page_links('http://duoduovision.diandian.com/'))
    #pprint.pprint(len(get_img_links('http://duoduovision.diandian.com/post/2012-04-10/19246614')))

    print 'start: ', time.asctime()
    url_param = 'http://duoduovision.diandian.com/page/%d'
    for i in range(20, 21):
        url = url_param % (i)
        fronter(url)
    print 'end: ', time.asctime()
