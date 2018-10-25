# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:48
# @Author  : xuzh
# @Project: KGCompleter

import re
import bs4

def extract_tag(s):
    res_str = r'<.*?>(.*?)</.*?>'
    tmp_str = re.findall(res_str, s, re.S | re.M)
    if tmp_str is not None and tmp_str != []:
        return tmp_str[0]
    else:
        return s

def clean_str(s):
    if isinstance(s, bs4.element.Tag):
        s = extract_tag(s)
    elif isinstance(s, list):
        s = [clean_str(x.string) for x in s]
        s = "".join(s)
    if not isinstance(s, str):
        return ""
    return s.replace("\n", "").strip()

