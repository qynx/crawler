HOST = "m.huaxiangju.com"
SCHEMA = "https://"
CHARSET = "gbk"
LIST_A_XPATH = '//ul[@class="chapter"]//li//a' # 章节列表标签a xpath
CONTENT_XPATH = '//div[@id="nr"]' #具体章节页 章节的xpath
NEXT_PAGE_XPATH = "" # 下一页xpath a
NEXT_PAGE_PATTERN = "https://m.huaxiangju.com/26392_{next_page_id}/"
START_ID = 1