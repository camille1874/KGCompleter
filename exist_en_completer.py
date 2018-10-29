# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
from baike_crawler import get_tuple
from tools import DB_util
import codecs
import json


# 因根据<实体，关系>直接获取mongoDB所有对应值效率较低，改成根据知识库三元组遍历。
# attr_record rel_record记录遍历历史。
# kep_rel字典记录已经爬取过的关系内容。
def check_result():
    m_collection = DB_util.stat()
    compare_file = codecs.open("compare_file.txt", mode="w", encoding="utf-8")
    # i = 0
    cursor = m_collection.find()
    keep_rel = {}
    entity_record = ""
    rel_record = []
    for document in cursor:
        # if i == 10:
        #     break
        m_tuple = document
        del m_tuple["_id"]
        entity = m_tuple["head"]
        rel = m_tuple["relation"]
        new_tuple = m_tuple
        rel_record.append(rel)
        if entity in keep_rel:
            rels = keep_rel[entity]
        else:
            keep_rel[entity] = {}
            rels = {}
        if rel in rels:
            new_tuple["tail"] = rels[rel]
        else:
            try:
                record = get_tuple(entity, rel)
                new_tuple = record[0]
                # print(record[1])
                rels[rel] = new_tuple["tail"]
                keep_rel[entity] = rels
            except Exception as e:
            #     TODO:记录没有处理好的实体关系。因为更新后被删除而导致的不一致不用写入数据库
                print(e)
                continue

        if not ((m_tuple["tail"] in new_tuple["tail"]) or (m_tuple["tail"] == new_tuple["tail"])):
            compare_file.write("不一致的数据库知识条目：" + json.dumps(m_tuple, ensure_ascii=False) + "\n"
                               + "新/已爬取知识集合：" + json.dumps(new_tuple, ensure_ascii=False) + "\n\n")
            compare_file.flush()
            # i += 1
        if entity_record != "" and entity != entity_record:
            new_record = {"head": entity_record}
            for tmp in keep_rel[entity_record]:
                if tmp not in rel_record:
                    new_record["relation"] = tmp
                    new_record["tail"] = keep_rel[entity_record][tmp]
                    compare_file.write("新/已爬取的数据库不存在的条目：" + json.dumps(new_record, ensure_ascii=False) + "\n\n")
            rel_record = []
            entity_record = entity
