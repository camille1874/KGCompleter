# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:23
# @Author  : xuzh
# @Project: KGCompleter

import re
from bs4 import BeautifulSoup
import requests, time


def get_html_baike(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_baike = BeautifulSoup(requests.get(url=url, headers=headers).content, "html.parser")
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup_baike.prettify())
    return soup_baike


def ptranswer(ans, ifhtml):
    result = ''
    for answer in ans:
        if ifhtml:
            print(answer)
        else:
            if answer == u'\n':
                continue
            p = re.compile('<[^>]+>')
            result += p.sub("", answer.string)
    return result
