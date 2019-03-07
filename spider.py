import json
import requests
from requests.exceptions import RequestException
import re, time

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>.*?：(.*/?)</p>.*?releasetime.*?>.*?：(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "index": item[0],
            "image": item[1],
            "title": item[2].strip(),
            "actor": item[3].strip(),
            "time": item[4].strip(),
            "score": item[5].strip()
        }

def write_to_file(content):
    with open("top100.txt", "a", encoding="utf-8") as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+ "\n")

def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
if __name__ == "__main__":
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)