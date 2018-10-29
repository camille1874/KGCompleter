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
                if bI.name == "dt":
                    tmp_name = ""
                    for bi in bI.contents:
                        tmp_name += bi.string.strip().replace(" ", "")
                elif bI.name == "dd":
                    contents = T.clean_str(bI.contents)
                    if isinstance(contents, str) and contents != "":
                        contents = [contents]
                    elif isinstance(contents, list):
                        contents = [x for x in contents if x != ""]
                        if len(contents) == 0:
                            continue
                    info[tmp_name] = contents

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
    elif attr == "BaiduCARD":
        # TODO: 长度阈值暂时设为1000，直接截取
        answers = []
        intro = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if not meta is None:
            intro = meta["content"]
        if intro is None or intro == "":
            log += attr + "-找不到\n"
        answers.append(clean_str(intro[:1000]))
        m_tuple['tail'] = answers
    else:
        result = query(entity, attr)
        if result == "":
            log += entity + "-找不到\n"
        m_tuple['tail'] = result[0]
        log += result[1]
    return m_tuple, log