# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
from BaikeCrawler import get_tuple
from tools import DBUtil
import codecs
import json

from tools.DBUtil import get_relation_value


def check_result():
    m_collection = DBUtil.stat()
    compare_file = codecs.open("compare_file.txt", mode="w", encoding="utf-8")
    i = 0
    cursor = m_collection.find()
    keep_rel = {}
    for document in cursor:
        if i == 10:
            break
        if document["relation"] in keep_rel:
            break
        m_tuple = document
        del m_tuple["_id"]
        attr = m_tuple["head"]
        rel = m_tuple["relation"]
        m_result = get_relation_value(m_collection, attr, rel)
        new_tuple = get_tuple(attr, rel)[0]
        if not set(m_result["tail"]) == set(new_tuple["tail"]):
            compare_file.write("数据库知识值集合：" + json.dumps(m_result, ensure_ascii=False) + "\n"
                               + "新爬取知识值集合：" + json.dumps(new_tuple, ensure_ascii=False) + "\n")
            compare_file.flush()
            print(m_tuple)
            print(new_tuple)
            i += 1
