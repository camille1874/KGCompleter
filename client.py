# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:36
# @Author  : xuzh
# @Project: KGCompleter

import BaikeCrawler
from tools import text_processor as T

entity = input()
attr = input()
result = BaikeCrawler.query(entity, attr)
ans = result[0]
log = result[1]
print(ans, log)
result = BaikeCrawler.get_tuple(entity)
ans = result[0]
log = result[1]
print(ans, log)
