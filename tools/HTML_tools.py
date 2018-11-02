# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:23
# @Author  : xuzh
# @Project: KGCompleter
import random

from bs4 import BeautifulSoup
import requests, time


def get_html_baike(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    page = ''
    while page == '':
        try:
            # page = requests.get(url=url, allow_redirects=False, timeout=1, proxies=get_random_ip(), headers=headers)
            page = requests.get(url=url, allow_redirects=False, timeout=1, headers=headers)
            break
        except Exception as e:
            print(e)
            time.sleep(random.randint(0, 3))
            continue

    soup_baike = BeautifulSoup(page.content, "html.parser")
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup_baike.prettify())
    return soup_baike
