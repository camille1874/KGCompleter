# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:36
# @Author  : xuzh
# @Project: KGCompleter

# TODO: 定期备份和更新 mongodump -h "172.16.35.1:27017" -d "triple" -c "baidubaike" -o "E:\data\db"
# TODO: 多线程
# TODO: 查其他注意事项

# TODO: 多义问题 原始（mongoDB三元组就没有存实体URI）
from exist_en_completer import en_completer


ec = en_completer()
ec.check_result_from_web()
