import requests
from lxml.html import fromstring
from lxml.etree import tostring
import pymysql
import redis
import os
import time
import logging

from utils import Chapter, SQLALCHEMY_CONN

logging.basicConfig(level=logging.INFO)

redis_client = redis.Redis(db=2)
mysql_client = pymysql.connect(
                    host="127.0.0.1",
                    user="root",
                    password=os.environ.get("SQL_PASSWORD"),
                    db="qq",
                    charset="utf8"
)
sqlalchemyConn = SQLALCHEMY_CONN()


class Crawler():

    SCHEMA = "https://"
    HOST = "m.80txt.com"

    LIST_URL_KEY = "txt80_list"
    CHAPTER_URL_KEY = "txt80_chapter"

    INCRE_KEY = "txt80_incr"

    def __init__(self, start_url='https://m.80txt.com/30913/page-1.html'):
        self.start_url = start_url
        self.session = requests.Session()
        self.restart()
        redis_client.lpush(self.LIST_URL_KEY, start_url)

    def restart(self):
        redis_client.delete(self.INCRE_KEY)
        redis_client.delete(self.LIST_URL_KEY)
        redis_client.delete(self.CHAPTER_URL_KEY)

    def run(self):
        # self.chapter_run()
        while True:
            url = redis_client.lpop(self.LIST_URL_KEY)
            logging.info("run get url: %s" % url)
            if url is None:
                return
            url = url.decode("utf-8")
            self.crawl_chapter_url(url)
            self.chapter_task()

    def chapter_run(self):
        logging.info("start charpter_run")
        for i in range(5):
            executor.submit(self.chapter_task)

    def chapter_task(self):
        while True:
            url = redis_client.lpop(self.CHAPTER_URL_KEY)
            if url is None:
                return
                continue
            url = url.decode("utf-8")
            logging.info("chapter task get url: %s" %(url))
            self.crawl_chapter_content(url)

    def start(self):
        rsp = self.session.get(self.start_url)
        rsp.encoding = "utf-8"
        html = rsp.text
        
    def crawl_chapter_url(self, url):
        logging.info("ready to crawl [url:%s]" % url)
        rsp = self.session.get(url)
        logging.info("after crawl")
        rsp.encoding = "utf-8"
        _html = rsp.text
        root = fromstring(_html)
        hrefs = root.xpath('//div[@class="book_last"]//a//@href')
        next_page_a = root.xpath('//span[@class="right"]//a[@class="onclick"]//@href')
        if len(next_page_a)> 0:
            redis_client.lpush(self.LIST_URL_KEY, self.SCHEMA + self.HOST + next_page_a[0])
        chapter_urls = []
        for href in hrefs:
            _id = redis_client.incr(self.INCRE_KEY)
            href = self.SCHEMA + self.HOST + href + "#%s" % _id
            redis_client.lpush(self.CHAPTER_URL_KEY, href)
            chapter_urls.append(href)

    def crawl_chapter_content(self, url):
        _id = url.split("#")[-1]
        logging.info("ready to crawl [url:%s]" % url)
        r = self.session.get(url)
        logging.info("after crawl")
        r.encoding="utf-8"
        chapter_html = r.text
        chapter_root = fromstring(chapter_html)
        title = chapter_root.xpath("//h1//text()")[0]

        div_content = chapter_root.xpath('//div[@id="nr1"]')

        content = tostring(div_content[0], method="html", pretty_print=True, encoding="utf-8")
        content = content.decode("utf-8")
        content = content.replace("\xa0", "")
        content=content.replace("<br>", "")
        content=content.replace('<div id="nr1">', '')
        content=content.replace('</div>', "")

        session = sqlalchemyConn.DBSession()
        chapter = Chapter(chapter_id=_id, title=title, content=content)
        session.add(chapter)
        session.commit()

if __name__ == '__main__':
    crawler = Crawler(start_url='https://m.80txt.la/11155/page-1.html')
    crawler.run()