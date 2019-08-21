import requests
import pymysql
import os
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

def exports():
    with open("book.txt", "r") as f:
        book_id = f.readlines()[-1].strip()
    sql = 'select chapter_id, title, content from novel where book_id = "%s" order by chapter_id ' % book_id
    logging.info(sql)
    cursor = mysql_client.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    with open("name.txt", "w", encoding="utf-8") as f:
        for data in datas:
            f.write(data[1] + "\n\n")
            f.write(data[2].replace('<div id="content1">', ""))

if __name__ == "__main__":
    exports()
