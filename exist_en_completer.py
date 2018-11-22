# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
import datetime
import random
import sys
import time

from baike_crawler import trigger, get_knowledge, get_soup
from tools import DB_util
import codecs
import json

from tools.DB_util import insert_tuple, update_tuple, insert_knowledge

class en_completer:
    def __init__(self):
        self.m_collection = DB_util.stat()
        self.cursor = self.m_collection.find()
        # self.compare_file = codecs.open("compare_file.txt", mode="a+", encoding="utf-8")
        self.record_file = codecs.open("record_file.txt", mode="a+", encoding="utf-8")
        self.record_file.seek(0)
        records = self.record_file.readlines()
        self.last_entity = ""
        self.entites = set()
        self.buffer_list = []
        self.flush_flag = True
        if records:
            tmp_entities = [x.strip().split("\t")[0] for x in records]
            self.last_entity = tmp_entities[-1]
            self.entites = set(tmp_entities)
        self.init_list = codecs.open(".\\resources\\SynonDic.txt", encoding="utf-8").readlines()
        tmp_list = []
        for l in self.init_list:
            tmp_list += l.split(" ")
        self.init_list = random.sample(tmp_list, 50)
        # self.synon_lists = build_synon_dict(".\\resources\\SynonDic.txt")

    # 根据web页面遍历, 触发也是根据网页链接：
    # kb存在web不存在：不改变
    # kb和web不一致：按web更新
    # kb不存在web存在：写入(新关系-单条三元组；新实体-整条知识)
    def check_result_from_web(self):
        entity_list = []
        if self.last_entity:
            entity_list = [self.last_entity]
        entity_list += list(set(self.init_list).difference(self.entites))
        while entity_list:
            en = entity_list[0]
            stat_time = time.time()
            end_time = stat_time
            r_code = None
            self.flush_flag = False
            # synon_entities = get_synons(en, self.synon_lists) 质量不高，不适合用来处理实体或关系
            soup = get_soup(en)
            result = get_knowledge(soup, en)
            web_tuples = result[0]
            log = result[1]
            db_tuples = list(self.m_collection.find({"head": en}))

            if not web_tuples:
                entity_list.remove(en)
                continue
            else:
                try:
                    if not db_tuples:
                        r_code = insert_knowledge(self.m_collection, web_tuples)
                    else:
                        for rel in web_tuples["relation"].items():
                            if not rel[1]:
                                continue
                            db_tuple = [x["tail"] for x in db_tuples if x["relation"] == rel[0]]
                            new_tuple = {"head": web_tuples["head"], "relation": rel[0], "tail": rel[1]}
                            if not db_tuple:
                                r_code = insert_tuple(self.m_collection, new_tuple)
                            elif isinstance(db_tuple[0], list) or not set(rel[1]) == set(db_tuple):
                                r_code = update_tuple(self.m_collection, new_tuple, len(db_tuple))
                except Exception as e:
                    # print(e)
                    print(web_tuples)
                    print(db_tuples)
                    return None
            if r_code:
                self.record_file.write("".join(self.buffer_list))
                self.flush_flag = True
                self.buffer_list.clear()
                self.record_file.flush()
            tmp_set = trigger(soup, en).difference(self.entites)
            if tmp_set and en != self.last_entity:
                record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.buffer_list.append(en + "\t" + record_time + "\n")
                self.entites.add(en)
                # 防止无法触发后续查询的实体成为last_entity
            # if len(entity_list) < 100:
            #     entity_list += list(tmp_set)
            entity_list.remove(en)
            entity_list += list(tmp_set)[:200]
            end_time = time.time()
            if end_time - stat_time > 2:
                return None


    # 根据知识库三元组遍历, 触发也是根据tail实体，该方法不适用：
    # 按<实体，关系>直接检索mongoDB所有对应值效率较低，
    # 遍历的话知识库存储是乱序的，
    # 而按网页遍历更方便收集同一实体的信息。
    # def check_result_from_db(self):
