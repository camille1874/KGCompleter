# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:36
# @Author  : xuzh
# @Project: KGCompleter

import BaikeCrawler
from tools import text_processor as T

entity = input()
attr = input()
ans = T.clean_str(BaikeCrawler.query(entity, attr))
print(ans)
