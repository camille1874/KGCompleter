# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:23
# @Author  : xuzh
# @Project: KGCompleter
import random

from bs4 import BeautifulSoup
import requests, time

headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False


def get_html_baike(url):
    page = ''
    while page == '':
        try:
            # page = requests.get(url=url, timeout=1, proxies=get_random_ip(), headers=headers)
            page = requests.get(url=url, timeout=1, headers=headers)
            break
        except Exception as e:
            # print(e)
            time.sleep(random.randint(0, 5))
            continue

    soup_baike = BeautifulSoup(page.content, "html.parser")
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup_baike.prettify())
    return soup_baike

def get_hot_topic():
    page = ''
    menu = []
    hot = set()
    url = 'https://top.sogou.com/'
    print("Getting hot topic seeds...")
    try:
        page = requests.get(url=url, timeout=1, headers=headers)
    except Exception as e:
        print(e)
    soup_menu = BeautifulSoup(page.content, "html.parser")
    # print(soup_menu.prettify())
    menu_list = soup_menu.find(class_='menu')
    for m in menu_list:
        href = m['href']
        if 'all_1' in href:
            menu.append(href)
    for m in menu:
        for i in range(1, 4):
            try:
                topic_page = requests.get(url=url + m.replace("1", str(i)), timeout=1, headers=headers)
            except Exception as e:
                print(e)
            soup_topic = BeautifulSoup(topic_page.content, "html.parser")
            hot_list = soup_topic.find_all(class_='p1')
            for p in hot_list:
                hot.add(p.text)
    return list(hot)
# print(get_hot_topic())