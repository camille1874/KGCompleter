# -*- encoding: utf-8 -*-
# @Time    : 2018/10/25 10:16
# @Author  : xuzh
# @Project: KGCompleter

from tools import HTML_tools as To
from tools import text_processor as T
import bs4
import re

from tools.text_processor import clean_str


def get_info(info_block):
    info = {}
    for bI_LR in info_block.contents:
        try:
            for bI in bI_LR:
                if not (isinstance(bI, bs4.element.Tag) and bI.name):
                    continue
                if bI.name == "dt":
                    tmp_name = ""
                    for bi in bI.contents:
                        tmp_name += bi.string.strip().replace(" ", "")
                elif bI.name == "dd":
                    contents = T.clean_str(bI.contents)
                    if isinstance(contents, str) and contents:
                        contents = [contents]
                    elif isinstance(contents, list):
                        contents = [x for x in contents if x]
                        if not contents:
                            continue
                    info[tmp_name] = contents

        except Exception as e:
            continue
    return info


def get_soup(entity):
    entity_uri = 'http://baike.baidu.com/item/' + entity
    soup = To.get_html_baike(entity_uri)
    return soup


# <关系， 值>
def get_knowledge(soup, entity):
    log = "查询百科列表实体:" + entity + "\n"
    info_block = soup.find(class_='basic-info cmn-clearfix')
    tuples = {}
    if not info_block:
        log += entity + "-找不到\n"
    else:
        tuples = {"head": entity}
        tmp = get_info(info_block)
        if not tmp:
            log += entity + "-没有Infobox属性或关系\n"
        tmp["BaiduTAG"] = get_special_tuple(soup, entity, "BaiduTAG")[0]["tail"]
        tmp["BaiduCARD"] = get_special_tuple(soup, entity, "BaiduCARD")[0]["tail"]
        tuples["relation"] = tmp
    return tuples, log


# {'head':'', 'relation':'', 'tail', ''}
def get_special_tuple(soup, entity, attr):
    log = "查询百科列表实体:" + entity + "\n"
    # print(soup.prettify())
    m_tuple = {'head': entity, 'relation': attr}
    if attr == "BaiduTAG":
        answers = []
        tags = soup.find_all(class_='taglist')
        if not tags:
            log += attr + "-找不到\n"
        else:
            for tag in tags:
                answers.append(clean_str(tag.get_text()))
        m_tuple['tail'] = answers
    elif attr == "BaiduCARD":
        # 长度阈值暂时设为1000，选到阈值之内最后一句。
        answers = []
        intro = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            intro = meta["content"]
        if not intro:
            log += attr + "-找不到\n"
        answers.append(clean_str(intro[:intro[:1000].rfind("。") + 1]))
        m_tuple['tail'] = answers
    else:
        return None
    return m_tuple, log


def trigger(soup, entity):
    # print(soup.prettify()
    seeds = set()
    sources = soup.find_all("a", attrs={"href": re.compile(r'/item/.*')})
    entities = soup.find_all("div", attrs={"class": "name"})
    for item in sources:
        if len(seeds) > 100:
            return seeds
        if item.get("data-lemmaid") and item.string:
            seeds.add(item.string)
    for item in entities:
        if len(seeds) > 100:
            return seeds
        seeds.add(item["title"])
    if entity in seeds:
        seeds.remove(entity)
    return seeds
