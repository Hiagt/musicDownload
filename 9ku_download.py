# -*- coding: utf-8 -*-

"""
@Time    : 2020/4/8 8:38 下午
@Author  : Hiagt
@File    : 9ku_download.py
@Software: PyCharm
"""
import os
import simplejson as json
import requests
from bs4 import BeautifulSoup
import math


def get_sid_by_singer(url):
    song_list = list()
    req = requests.get(url).text
    soup = BeautifulSoup(req, "html5lib")
    find_a = soup.find_all('a')
    for i in find_a:
        href = i.get('href')
        if href and 'play/' in href:
            song_list.append(int(href.split('/')[-1].split('.')[0]))
    return set(song_list)


def get_download_js(sid_list):
    info_js_list = list()
    for i in sid_list:
        tpath = math.floor(i / 1000) + 1
        js_url = "http://www.9ku.com/html/playjs/" + str(tpath) + "/{}.js".format(i)
        info_js_list.append(js_url)
    return info_js_list


def download(url, save_path):
    req = requests.get(url).content
    req = req.decode('unicode_escape')
    req = req.split('(')[1].split(')')[0]
    req = json.loads(req)
    download_url = req.get('wma')
    singer = req.get('singer')
    m_name = req.get('mname')

    dst_path = os.path.join(save_path, singer)
    if os.path.exists(dst_path):
        pass
    else:
        os.makedirs(dst_path)

    save_path = os.path.join(dst_path, '{} - {}.mp3'.format(singer, m_name))

    m_req = requests.get(download_url, stream=True)
    # with open(save_path, 'wb') as f:
    #     for i in res.iter_content():
    #         f.write(i)
    with open(save_path, 'ab') as f:
        f.write(m_req.content)
    pass


def download_by_singer_page(url, save_path):
    sid_list = get_sid_by_singer(url)
    info_js_list = get_download_js(sid_list)
    for i in info_js_list:
        download(i, save_path)
    pass


if __name__ == '__main__':
    url = 'http://www.9ku.com/geshou/1991.htm'
    save_path = '/Volumes/ssd_t5/music'
    download_by_singer_page(url, save_path)

