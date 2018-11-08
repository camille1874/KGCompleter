# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:48
# @Author  : xuzh
# @Project: KGCompleter

import re
import bs4


def extract_tag(s):
    res_str = r'<.*?>(.*?)</.*?>'
    tmp_str = re.findall(res_str, s, re.S | re.M)
    if tmp_str:
        return tmp_str[0]
    else:
        return s


def clean_str(s):
    if isinstance(s, bs4.element.Tag):
        s = extract_tag(s)
    elif isinstance(s, list):
        s = [clean_str(x) for x in s]
    elif isinstance(s, str):
        s = s.replace("\n", "").replace("\t", "").strip()
        # pattern = re.compile(r'\s+')
        # s = re.sub(pattern, '', s)
    else:
        s = ""
    return s
