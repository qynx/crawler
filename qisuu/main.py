import click
import logging
import redis
import sys
import time
import umsgpack
import uuid
from lxml.html import fromstring
from lxml.etree import tostring
sys.path.insert(0, "..")
from utils.request import Request
from utils.sql_conn import Chapter
from utils.sql_conn import SQLALCHEMY_CONN

logging.basicConfig(
    level=logging.INFO
)

book_id = str(uuid.uuid4())[0:32]
with open("book.txt", "a") as f:
    f.write(book_id + "\n")
logging.info("book-id: %s" % book_id)
sqlalchemyConn = SQLALCHEMY_CONN()
redisClient = redis.Redis(db=2)

'''
nbiquge 结构：
    列表页 包含所有的章节链接
命令行单次抓取 没有加入异常处理
'''
class Crawler():

    HOST = "www.qisuu.la"
    SCHEMA = "https://"

    LIST_URL_KEY = HOST + ".list_url"
    CHAPTER_URL_KEY = HOST + ".chapter_url"
    # 记录章节顺序
    INCR_KEY = HOST + ".incr_key"

    def __init__(self, start_url="https://www.nbiquge.com/7_7295/"):
        logging.info("crawler init...")
        self.start_url = start_url
        self.request = Request()
        redisClient.lpush(self.LIST_URL_KEY, start_url)

    def run(self):
        self.consume_list()

    def consume_list(self):
        '''
        串行取数据 每次从redis中取出一个list 抓取相应章节后
        再抓取下一页的链接 如果取不到新的链接 则程序结束
        '''
        list_url = redisClient.rpop(self.LIST_URL_KEY)
        if list_url is None:
            return
        logging.info("get url %s", list_url)
        self.parse_list(list_url)

    def parse_list(self, url):
        logging.info("parse_list get url: %s" % url.decode("utf-8"))
        rsp = self.request.get(url.decode("utf-8"))
        rsp.encoding = "utf-8"  # 指定rsp的编码方式（否则解码后会有乱码）
        root = fromstring(rsp.text)
        # import pdb; pdb.set_trace()
        list_div = root.xpath('//div[@class="pc_list"]')[1]
        chapters = list_div.xpath(".//li//a")
        logging.info("get %s chapter" % len(chapters))
        for chapter in chapters:
            chapter_id = redisClient.incr(self.INCR_KEY)
            task = {
                "href": self.start_url + chapter.xpath(".//@href")[0],
                "name": chapter.xpath("string(.)"),
                "id": chapter_id
            }
            redisClient.lpush(self.CHAPTER_URL_KEY, umsgpack.packb(task))
            if chapter_id % 10 == 0:
                '''
                每10章
                '''
                logging.info("now chapter_id: %s" % chapter_id)
                self.consume_chapter()
            time.sleep(1)

    def consume_chapter(self):
        while True:
            #import pdb; pdb.set_trace()
            task = redisClient.lpop(self.CHAPTER_URL_KEY)
            if task is None:
                return
            self.consume_single_chapter(task)

    def consume_single_chapter(self, task):
        task = umsgpack.unpackb(task)
        logging.info("consume_single_chapter get a task [url: %s]" % task["href"])
        rsp = self.request.get(task["href"])
        rsp.encoding = "utf-8"
        root = fromstring(rsp.text)
        content_div = root.xpath('//div[@id="content1"]')[0]

        content = tostring(content_div, method="html", pretty_print=True, encoding="utf-8")
        content = content.decode("utf-8")
        content = content.replace("<br>", "")
        content = content.replace("\xa0", "")
        content = content.replace('<div id="content1">', '')
        content = content.replace('</div>', "")
        # import pdb; pdb.set_trace()
        sqlSession = sqlalchemyConn.DBSession()
        chapter = Chapter(chapter_id=task["id"],
                          title=task["name"], 
                          content=content,
                          book_id=book_id,
                          site=self.HOST)
        sqlSession.add(chapter)
        sqlSession.commit()

    @classmethod
    def restart(self):
        '''
        清除数据
        '''
        redisClient.delete(self.LIST_URL_KEY)
        redisClient.delete(self.CHAPTER_URL_KEY)
        redisClient.delete(self.INCR_KEY)

@click.group()
def cli():
    pass

@cli.command()
def debug():
    Crawler.restart()
    crawler = Crawler(start_url='https://www.qisuu.la/du/6/6830/')
    crawler.run()

@cli.command()
@click.option("--url")
def run(url):
    Crawler.restart()
    crawler = Crawler(url)
    crawler.run()

    
if __name__ == "__main__":
    cli()