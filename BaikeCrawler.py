# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:16
# @Author  : xuzh
# @Project: KGCompleter

from tools import HTML_tools as To

def get_info(basicInfo_block):
    info = {}
    for bI_LR in basicInfo_block.contents:
        try:
            for bI in bI_LR:
                if bI.name == None:
                    continue
                if bI.name == 'dt':
                    tempName = ''
                    for bi in bI.contents:
                        tempName += bi.string.strip().replace(" ", "")
                elif bI.name == 'dd':
                    info[tempName] = bI.contents
        except Exception as e:
            continue
    return info

def query(entity, attr):
    entity_uri = 'http://baike.baidu.com/item/' + entity
    result = '查询百科列表实体:' + entity_uri + '\n'
    soup = To.get_html_baike(entity_uri)
    basicInfo_block = soup.find(class_='basic-info cmn-clearfix')
    if basicInfo_block == None:
        return result + entity + "-找不到\n"
    else:
        info = get_info(basicInfo_block)
        if attr in info:
            return info[attr]
        else:
            return result + '属性' + attr + '-找不到\n'

