# -*- encoding: utf-8 -*-
# @Time    : 2018/11/1 14:11
# @Author  : xuzh
# @Project: KGCompleter
import codecs
import os


def build_synon_dict(file_name):
    f = codecs.open(os.path.join("..\\resources", file_name), encoding="utf-8")
    lines = f.readlines()
    synon_lists = [x.strip().split(" ") for x in lines]
    return synon_lists


def get_synons(word, synon_lists):
    result = []
    for slist in synon_lists:
        if word in slist:
            result += slist
    return result


# synon_lists = build_synon_dict("SynonDic.txt")
# print(get_synons("家", synon_lists))
