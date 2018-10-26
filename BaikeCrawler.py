# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:16
# @Author  : xuzh
# @Project: KGCompleter

from tools import HTML_tools as To
from tools import text_processor as T
import bs4

from tools.text_processor import clean_str


def get_info(basicInfo_block):
    info = {}
    for bI_LR in basicInfo_block.contents:
        try:
            for bI in bI_LR:
                if not isinstance(bI, bs4.element.Tag) or bI.name is None:
                    continue
                if bI.name == 'dt':
                    tempName = ''
                    for bi in bI.contents:
                        tempName += bi.string.strip().replace(" ", "")
                elif bI.name == 'dd':
                    if not tempName in info:
                        info[tempName] = T.clean_str(bI.contents)
                    else:
                        info[tempName].append(T.clean_str(bI.contents))
        except Exception as e:
            continue
    return info


# 值
def query(entity, attr):
    info, log = get_knowledge(entity)
    answer = ""
    log += "查询属性/关系:" + attr + "\n"
    if attr in info:
        answer = info[attr]
    else:
        log += "属性" + attr + '-找不到\n'
    return answer, log


# <关系， 值>
def get_knowledge(entity):
    entity_uri = 'http://baike.baidu.com/item/' + entity
    log = "查询百科列表实体:" + entity_uri + "\n"
    soup = To.get_html_baike(entity_uri)
    info_block = soup.find(class_='basic-info cmn-clearfix')
    tuples = {}
    if info_block is None:
        log += entity + "-找不到\n"
    else:
        tuples = get_info(info_block)
        if tuples == {}:
            log += entity + "-没有属性或关系\n"
    return tuples, log


# {'head':'', 'relation':'', 'tail', ''}
def get_tuple(entity, attr):
    entity_uri = 'http://baike.baidu.com/item/' + entity
    log = "查询百科列表实体:" + entity_uri + "\n"
    soup = To.get_html_baike(entity_uri)
    # print(soup.prettify())
    m_tuple = {'head': entity, 'relation': attr}
    if attr == "BaiduTAG":
        answers = []
        tags = soup.find_all(class_='taglist')
        if tags is None:
            log += attr + "-找不到\n"
        else:
            for tag in tags:
                answers.append(clean_str(tag.get_text()))
        m_tuple['tail'] = answers
    else:
        info_block = soup.find(class_='basic-info cmn-clearfix')
        if info_block is None:
            log += entity + "-找不到\n"
        else:
            result = query(entity, attr)
            m_tuple['tail'] = result[0]
            log += result[1]
    return m_tuple, log
