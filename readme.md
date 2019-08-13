## 小说网站爬虫（学习娱乐）

### 依赖

- redis
- mysql

### 说明

1. 执行sql.sql 
2. 将sql root用户的密码配置到环境变量中 或手动修改 utils/sql_conn.py
3. 程序入口提供列表首页链接

### 网站列表

1. txt80

可在pc端搜索 site:m.80txt.la {小说书名} 找到链接 或直接在移动端搜索

> example: https://m.80txt.la/11155/page-1.html

2. nbiquge

> example: https://www.nbiquge.com/7_7295/
> python main.py run --url https://www.nbiquge.com/7_7295/
3.  