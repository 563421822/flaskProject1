import requests
from bs4 import BeautifulSoup

url = "http://read.nlc.cn/allSearch/searchList?searchType=12&showType=1&pageNo=1"  # 中国国家图书馆

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36"
}
for index, item in enumerate(range(5)):
    url = "http://read.nlc.cn/allSearch/searchList?searchType=12&showType=1&pageNo=" + str(index)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # 通过BeautifulSoup的find和find_all方法获取需要的数据
    titles = soup.find_all("span", class_="tt")
    # 打印获取到的标题
    for title in titles:
        print(title.get_text())
