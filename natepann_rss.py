import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time

BASE_URL = "https://pann.nate.com"
RANKING_URL = f"{BASE_URL}/talk/ranking/d"
HEADERS = {"User-Agent": "Mozilla/5.0"}

res = requests.get(RANKING_URL, headers=HEADERS)
soup = BeautifulSoup(res.text, "html.parser")

fg = FeedGenerator()
fg.title("네이트판 실시간 인기글")
fg.link(href=RANKING_URL, rel="alternate")
fg.description("네이트판 오늘의 인기글을 RSS로 제공합니다.")

posts = soup.select(".list li a")[:10]

for post in posts:
    title = post.get_text(strip=True)
    link = BASE_URL + post['href']

    post_res = requests.get(link, headers=HEADERS)
    post_soup = BeautifulSoup(post_res.text, "html.parser")

    content_tag = post_soup.select_one(".postContent")
    if content_tag:
        content_html = str(content_tag)
    else:
        content_html = "본문을 불러오지 못했습니다."

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.guid(link)
    fe.description(content_html)

    time.sleep(1)

fg.rss_file("natepann_rss.xml")
print("✅ natepann_rss.xml 파일 생성 완료!")
