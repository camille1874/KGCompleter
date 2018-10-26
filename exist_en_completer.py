# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
from BaikeCrawler import get_tuple
from tools import DBUtil
import codecs
import json


def check_result():
    m_collection = DBUtil.stat()
    compare_file = codecs.open("compare_file.txt", mode="w", encoding="utf-8")
    i = 0
    cursor = m_collection.find()
    keep_rel = {}
    attr_record = ""
    rel_record = []
    for document in cursor:
        if i == 10:
            break
        m_tuple = document
        del m_tuple["_id"]
        attr = m_tuple["head"]
        rel = m_tuple["relation"]
        new_tuple = m_tuple
        rel_record.append(rel)
        if attr in keep_rel:
            rels = keep_rel[attr]
        else:
            keep_rel[attr] = {}
            rels = {}
        if rel in rels:
            new_tuple["tail"] = rels[rel]
        else:
            new_tuple = get_tuple(attr, rel)[0]
            rels[rel] = new_tuple["tail"]
            keep_rel[attr] = rels

        # m_result = get_relation_value(m_collection, attr, rel)
        # if not set(m_result["tail"]) == set(new_tuple["tail"]):
        if not m_tuple["tail"] in new_tuple["tail"]:
            compare_file.write("不一致的数据库知识条目：" + json.dumps(m_tuple, ensure_ascii=False) + "\n"
                               + "新/已爬取知识集合：" + json.dumps(new_tuple, ensure_ascii=False) + "\n\n")
            compare_file.flush()
            print(m_tuple)
            print(new_tuple)
            i += 1
        if attr != attr_record:
            new_record = {"head": attr}
            for tmp in keep_rel[attr]:
                if tmp not in rel_record:
                    new_record["relation"] = tmp[0]
                    new_record["tail"] = tmp[1]
                    compare_file.write("新/已爬取的数据库不存在的条目：" + json.dumps(new_record, ensure_ascii=False) + "\n\n")
            rel_record = []
        attr_record = attr
