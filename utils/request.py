# 2019-08-11
import requests
import time
from .Reporter import BaseReporter, InfluxReporter
import logging

class Request():

    def __init__(self):
        '''
        考虑到session的特性 对同一host使用一个session
        可以极大提高下载速度
        '''
        self.session = requests.Session()
        self.get_reporter()

    def get_reporter(self):
        reporter = InfluxReporter()
        try:
            reporter.ping()
        except Exception as e:
            print(e)
            reporter = BaseReporter()
        self.reporter = reporter

    def get(self, *args, **kw):
        logging.info("url: %s" % args[0])
        kw["timeout"] = (5, 10)
        kw["headers"] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        start = time.time()
        rsp = self.session.get(*args, **kw)
        end = time.time()
        self.reporter.report_lag("nbiquge", end-start)
        return rsp

    def post(self, *args, **kw):
        kw["timeout"] = (5, 10)
        start = time.time()
        rsp = self.session.post(*args, **kw)
        end = time.time()
        self.reporter.report_lag("nbiquge", end-start)
        return rsp