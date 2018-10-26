# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:00
# @Author  : xuzh
# @Project: KGCompleter
import time

from pymongo import MongoClient
from bson.code import Code


def stat():
    try:
        with MongoClient("mongodb://172.16.35.1:27017") as client:
            db = client['triple']
            m_collection = db['baidubaike']
            return m_collection
    except Exception as e:
        print(e)


def get_tuple_db(m_collection):
    tuples = []
    with m_collection.find() as cursor:
        for document in cursor:
            m_tuple = document
            del m_tuple['_id']
            tuples.append(m_tuple)
    return tuples


def get_value(m_collection, entity):
    cursor = m_collection.find({"head": entity})
    values = {}
    for doc in cursor:
        values[doc['relation']] = (doc['tail'])
    return values


def get_relation_value(m_collection, entity, attr):
    start = time.time()
    cursor = m_collection.find({"head": entity, "relation": attr})
    # pipeline = [{'$match': {'head': entity, 'relation': attr}}]
    # cursor = m_collection.aggregate(pipeline)
    values = {}
    answers = []
    values["head"] = entity
    values["relation"] = attr
    for doc in cursor:
        answers.append(doc['tail'])
    values["tail"] = answers
    total = (time.time() - start)
    print(total)
    return values


collection = stat()
result = get_relation_value(collection, "!DOCTYPE", "BaiduTAG")
print(result)
