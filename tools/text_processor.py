# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:48
# @Author  : xuzh
# @Project: KGCompleter

def clean_str(s):
    if isinstance(s, list):
        s = [clean_str(x) for x in s]
        s = "".join(s)
    if not isinstance(s, str):
        return ""
    return s.replace("<a>", "").replace("</a>", "").replace("<", "").replace(">", "").replace("\n", "").strip()

