# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:36
# @Author  : xuzh
# @Project: KGCompleter

import baike_crawler
from exist_en_completer import en_completer


# entity = input()
# attr = input()
# ans, log = BaikeCrawler.query(entity, attr)
# print(ans, log)
# ans, log = BaikeCrawler.get_knowledge(entity)
# print(ans, log)
ec = en_completer()
ec.check_result_from_web()
