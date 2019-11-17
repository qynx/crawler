import requests
from lxml.html import fromstring
from lxml.etree import tostring
import pymysql
import redis
import os
import sys
import time
import logging
logging.basicConfig(level=logging.INFO)

mysql_client = pymysql.connect(
                    host="127.0.0.1",
                    user="root",
                    password=os.environ.get("SQL_PASSWORD"),
                    db="qq",
                    charset="utf8"
)

def exports(book_id):
    sql = 'select chapter_id, title, content from novel  where book_id = "%s" order by chapter_id' % book_id
    cursor = mysql_client.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    with open("name.txt", "w", encoding="utf-8") as f:
        for data in datas:
            f.write(data[1] + "\n\n")
            f.write(data[2])

if __name__ == "__main__":
    
    exports(sys.argv[1])
