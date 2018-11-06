# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:00
# @Author  : xuzh
# @Project: KGCompleter
import time

from pymongo import MongoClient


def stat():
    try:
        with MongoClient("mongodb://172.16.35.1:27017") as client:
            db = client['triple']
            m_collection = db['baidubaike']
            return m_collection
    except Exception as e:
        print(e)


buffer = []


def check_insert(m_collection):
    global buffer
    if len(buffer) >= 500:
        result = m_collection.insert(buffer)
        buffer = []
        return result
    else:
        return None


def insert_tuple(m_collection, m_tuple):
    tuples = []
    tmp_tuple = {"head": m_tuple["head"], "relation": m_tuple["relation"]}
    if len(m_tuple["tail"]) == 0:
        return None
    for answer in m_tuple["tail"]:
        tmp_tuple["tail"] = answer
        tuples.append(tmp_tuple.copy())
    # return m_collection.insert(tuples)
    global buffer
    buffer += tuples
    return check_insert(m_collection)


# {head: head, relation: {relation : relation, tail: tail}}
def insert_knowledge(m_collection, entity_knowledge):
    tuples = []
    tmp_tuple = {"head": entity_knowledge["head"]}
    for knowledge in entity_knowledge["relation"].items():
        tmp_tuple["relation"] = knowledge[0]
        if len(knowledge[1]) == 0:
            continue
        for l in knowledge[1]:
            tmp_tuple["tail"] = l
            tuples.append(tmp_tuple.copy())
    # return m_collection.insert(tuples)
    global buffer
    buffer += tuples
    return check_insert(m_collection)


# 知识库可能存在<head, relation> 多条结果， 注意处理tail集合不一致的情况
def update_tuple(m_collection, m_tuple, db_tuple_len):
    if len(m_tuple["tail"]) == 0:
        # return m_collection.remove({"head": m_tuple["head"], "relation": m_tuple["relation"]})
        return None
    elif db_tuple_len == 1:
        return m_collection.update({"head": m_tuple["head"], "relation": m_tuple["relation"]},
                                   {"$set": {"tail": m_tuple["tail"][0]}})
    else:
        m_collection.remove({"head": m_tuple["head"], "relation": m_tuple["relation"]})
        return insert_tuple(m_collection, m_tuple)

# collection = stat()
# cursor = collection.find()
# cursor = [len(x) for x in cursor]
# print(cursor)
# result = cursor[cursor.find(max(cursor))]["tail"]
# print(result)
# print(len(result))
