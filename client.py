# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:36
# @Author  : xuzh
# @Project: KGCompleter

# TODO: 定期备份和更新 mongodump -h "172.16.35.1:27017" -d "triple" -c "baidubaike" -o "E:\data\db"
# TODO: 多线程
# TODO: 查其他注意事项

# TODO: 多义问题 原始（mongoDB三元组就没有存实体URI）
from exist_en_completer import en_completer
import atexit


def record_remaining():
    if not ec.flush_flag and ec.buffer_list:
        ec.record_file.write("".join(ec.buffer_list))
        ec.record_file.close()
    print("Record remaining entities...")


if __name__ == '__main__':
    ec = en_completer()
    print("Collecting Knowledge...")
    ec.check_result_from_web()
    print("Program finished...")
    atexit.register(record_remaining)
