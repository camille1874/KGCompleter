# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
import datetime

from baike_crawler import get_tuple, trigger, get_knowledge
from tools import DB_util
import codecs
import json


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

    # 根据知识库三元组遍历, 触发也是根据tail实体，该方法不适用：
    # 按<实体，关系>直接检索mongoDB所有对应值效率较低，
    # 遍历的话知识库存储是乱序的，
    # 而按网页遍历更方便收集同一实体的信息。
    def check_result_from_db(self):
        keep_rel = {}
        # tmp_last_entity = ""
        # entity_record = set()
        rel_record = set()
        for document in self.cursor:
            m_tuple = document
            del m_tuple["_id"]
            entity = m_tuple["head"]
            if entity in self.entites:
                continue
            rel = m_tuple["relation"]
            new_tuple = m_tuple
            rel_record.add(rel)
            print(document)
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

            # if entity != tmp_last_entity:
            #     if tmp_last_entity != "":
            #         new_record = {"head": tmp_last_entity}
            #         for tmp in keep_rel[tmp_last_entity]:
            #             if tmp not in rel_record:
            #                 new_record["relation"] = tmp
            #                 new_record["tail"] = keep_rel[tmp_last_entity][tmp]
            #                 self.compare_file.write(
            #                     "新/已爬取的数据库不存在的条目：" + json.dumps(new_record, ensure_ascii=False) + "\n\n")
            #                 self.compare_file.flush()
            #     rel_record.clear()
            #     tmp_last_entity = entity
            #     self.record_file.write(tmp_last_entity + "\t")
            #     self.record_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            #     self.record_file.write("\n")
            #     self.record_file.flush()

    # 不可行，太慢了
    def check_result_from_web(self):
        init_entity = "姚明"
        entity_list = [init_entity]
        while True:
            for en in entity_list:
                web_tuples = get_knowledge(en)[0]
                for rel in web_tuples["relation"]:
                    db_tuple = list(self.m_collection.find({"head": en, "relation": rel}))
                    print(db_tuple)
                    db_tuple = [x["tail"] for x in db_tuple]
                    if not set(web_tuples["relation"][rel]) == set(db_tuple):
                        self.compare_file.write("不一致的知识条目集：" + json.dumps(db_tuple, ensure_ascii=False) + "\n"
                                                + "新/已爬取的对应条目集：" + json.dumps(rel, ensure_ascii=False) + "\n\n")
                        self.compare_file.flush()
                if not en in self.entites:
                    self.record_file.write(en + "\t")
                    self.record_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    self.record_file.write("\n")
                    self.record_file.flush()
                entity_list.remove(en)
                entity_list.append(trigger(en))
