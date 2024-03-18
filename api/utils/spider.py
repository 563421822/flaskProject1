import json
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

url = "http://read.nlc.cn/user/category"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
html = soup.find_all("div", class_="module3")
root = []
# 所有一级类目
for i, md3_tag in enumerate(html):
    father = {'id': i, 'title': md3_tag.find("div", class_="tt").get_text()}
    # print(md3_tag.find("div", class_="tt").get_text())
    ul_li = md3_tag.find("ul", class_="ul1 Z_clearfix").find_all("li")
    father_son_array = []
    # 所有二级类目
    for idx, li in enumerate(ul_li):
        second_child = {'id': idx, 'title': li.find("span").get_text(), 'parent_id': i}
        item_title: str = li.find("span").get_text()
        item_url: str = li.find("a")["href"]
        if item_url.startswith("/"):
            item_url = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc + item_url
            print(item_title, item_url)
            # 访问二级类目中的连接查看所有图书
            resp = requests.get(item_url, headers=headers)
            sp = BeautifulSoup(resp.text, "html.parser")
            bk_ul = sp.find_all("ul")
            sec_arr = []
            for index, ul in enumerate(bk_ul):
                bk_li = ul.find_all("li")
                # 遍历二级类目下的所有图书
                for ix, book_li in enumerate(bk_li):
                    span = book_li.find("span")
                    if span:
                        li_url = book_li.find("a")["href"]
                        # print(item_url)
                        li_url = urlparse(resp.url).scheme + "://" + urlparse(resp.url).netloc + li_url
                        print("\tul索引" + str(index) + "：" + li_url + " " + span.get_text())
                        # 访问每本图书的链接获取详情
                        rsp = requests.get(li_url, headers=headers)
                        s = BeautifulSoup(rsp.text, "html.parser")
                        div = s.find("div", class_="XiangXi")
                        if div:
                            bk_entity = div.find_all("label")
                            entity = {"title": span.get_text()}
                            for lbl in bk_entity:
                                if "责任者" in lbl.get_text():
                                    entity["author"] = lbl.find("span").get_text()
                                if re.search(r'\b日期\b|\b时间\b', lbl.get_text()):
                                    entity["publication_date"] = lbl.find("span").get_text()
                                if re.search(r'\b简介\b|\b附注\b', lbl.get_text()):
                                    entity["description"] = lbl.find("span").get_text()
                            entity["type"] = idx
                            entity["href"] = li_url
                            sec_arr.append(entity)
                second_child["children"] = sec_arr
        father_son_array.append(second_child)
    father["children"] = father_son_array
    root.append(father)
# 将数据写入JSON文件
with open("../../static/kettle/my_data.json", "w") as f:
    json.dump(root, f)
print(json.dumps(root))
