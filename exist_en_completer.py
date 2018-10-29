# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
import datetime

from baike_crawler import get_tuple
from tools import DB_util
import codecs
import json


# 因根据<实体，关系>直接获取mongoDB所有对应值效率较低，
# 改成根据知识库三元组遍历,触发也是根据tail实体。
class en_completer:
    def __init__(self):
        self.m_collection = DB_util.stat()
        self.cursor = self.m_collection.find()
        self.compare_file = codecs.open("compare_file.txt", mode="a+", encoding="utf-8")
        self.record_file = codecs.open("record_file.txt", mode="a+", encoding="utf-8")
        records = self.record_file.readlines()
        self.last_entity = ""
        self.entites = []
        if len(records) > 0:
            self.entites = [x.split("\t")[0] for x in records]
            self.last_entity = self.entites[-1]


# 为便于管理，将每次重新启动后运行期间记录的实体和关系和本地历史记录区分开。
    def check_result(self):
        keep_rel = {}
        entity_record = ""
        rel_record = []
        for document in self.cursor:
            m_tuple = document
            del m_tuple["_id"]
            entity = m_tuple["head"]
            if entity in self.entites:
                continue
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
                self.compare_file.write("不一致的数据库知识条目：" + json.dumps(m_tuple, ensure_ascii=False) + "\n"
                                        + "新/已爬取的对应答案集：" + json.dumps(new_tuple, ensure_ascii=False) + "\n\n")
                self.compare_file.flush()

            if entity != entity_record:
                if entity_record != "":
                    new_record = {"head": entity_record}
                    for tmp in keep_rel[entity_record]:
                        if tmp not in rel_record:
                            new_record["relation"] = tmp
                            new_record["tail"] = keep_rel[entity_record][tmp]
                            self.compare_file.write(
                                "新/已爬取的数据库不存在的条目：" + json.dumps(new_record, ensure_ascii=False) + "\n\n")
                            self.compare_file.flush()
                rel_record = []
                entity_record = entity
                self.record_file.write(entity_record + "\t")
                self.record_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.record_file.write("\n")
                self.record_file.flush()
