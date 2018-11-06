# -*- encoding: utf-8 -*-
# @Time    : 2018/10/26 10:30
# @Author  : xuzh
# @Project: KGCompleter
import datetime

from baike_crawler import trigger, get_knowledge
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
        self.entites = []
        if len(records) > 0:
            self.entites = [x.strip().split("\t")[0] for x in records]
            self.last_entity = self.entites[-1]
        self.init_list = ["姚明", "王宝强", "中国", "清华大学", "上市", "腾讯", "郎咸平",
                          "金庸", "张艺谋", "陈奕迅", "鱼香肉丝", "台风山竹", "爵士舞", "重金属",
                          "世界杯", "游泳", "深圳", "宪法", "英国短毛猫", "黎曼猜想", "H7N9病毒",
                          "客家文化", "上海博物馆", "静安区", "北京市人民政府",
                          "卢浮宫", "阳江核电站", "低碳经济"]
        # self.synon_lists = build_synon_dict(".\\resources\\SynonDic.txt")

    # 根据web页面遍历, 触发也是根据网页链接：
    # kb存在web不存在：不改变
    # kb和web不一致：按web更新
    # kb不存在web存在：写入(新关系-单条三元组；新实体-整条知识)
    def check_result_from_web(self):
        entity_list = []
        if self.last_entity != "":
            entity_list = [self.last_entity]
        entity_list += list(set(self.init_list).difference(set(self.entites)))
        while len(entity_list) is not 0:
            en = entity_list[0]
            # synon_entities = get_synons(en, self.synon_lists) 质量不高，不适合用来处理实体或关系
            result = get_knowledge(en)
            web_tuples = result[0]
            log = result[1]
            db_tuples = list(self.m_collection.find({"head": en}))
            try:
                if len(web_tuples) == 0:
                    # self.compare_file.write(log)
                    pass
                elif len(db_tuples) == 0:
                    # self.compare_file.write(
                    #     "新/已爬取的数据库不存在的实体：" + json.dumps(web_tuples, ensure_ascii=False) + "\n")
                    # if insert_knowledge(self.m_collection, web_tuples) is not None:
                    #     self.compare_file.write("插入新实体条目集:" + "*" * 50)
                    # self.compare_file.write("\n")
                    # self.compare_file.flush()
                    insert_knowledge(self.m_collection, web_tuples)
                else:
                    for rel in web_tuples["relation"].items():
                        if len(rel[1]) == 0:
                            continue
                        db_tuple = [x["tail"] for x in db_tuples if x["relation"] == rel[0]]
                        new_tuple = {"head": web_tuples["head"], "relation": rel[0], "tail": rel[1]}
                        if len(db_tuple) == 0:
                            # self.compare_file.write( "新/已爬取的数据库不存在的实体-关系条目：" + web_tuples["head"] + "-" +
                            # json.dumps(rel, ensure_ascii=False) + "\n") if insert_tuple(self.m_collection,
                            # new_tuple) is not None: self.compare_file.write("插入新条目:" + "*" * 50)
                            # self.compare_file.write("\n") self.compare_file.flush()
                            insert_tuple(self.m_collection, new_tuple)
                        elif isinstance(db_tuple[0], list) or not set(rel[1]) == set(db_tuple):
                            # self.compare_file.write("不一致的实体关系:" + web_tuples["head"] + "-" + rel[0] + ":\n"
                            #                                                                           "知识库答案集：")
                            # if isinstance(db_tuple[0], list):
                            #     self.compare_file.write(" / ".join(db_tuple[0]) + "(列表)")
                            # else:
                            #     self.compare_file.write(" / ".join(db_tuple))
                            # self.compare_file.write("\n新/已爬取的答案集：")
                            # self.compare_file.write(" / ".join(rel[1]))
                            # if update_tuple(self.m_collection, new_tuple, len(db_tuple)) is not None:
                            #     self.compare_file.write("\n更新条目" + "*" * 50)
                            # self.compare_file.write("\n")
                            # self.compare_file.flush()
                            update_tuple(self.m_collection, new_tuple, len(db_tuple))
                if en not in self.entites:
                    self.record_file.write(en + "\t")
                    self.record_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    self.record_file.write("\n")
                    self.record_file.flush()
                    self.entites.append(en)
                entity_list += trigger(en)
                entity_list.remove(en)
            except Exception as e:
                print(e)
                print(web_tuples)
                print(db_tuples)
                continue

    # 根据知识库三元组遍历, 触发也是根据tail实体，该方法不适用：
    # 按<实体，关系>直接检索mongoDB所有对应值效率较低，
    # 遍历的话知识库存储是乱序的，
    # 而按网页遍历更方便收集同一实体的信息。
    # def check_result_from_db(self):
