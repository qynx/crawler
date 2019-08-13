# 2019-08-11
import requests
import time
from .Reporter import BaseReporter, InfluxReporter


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
        kw["timeout"] = (5, 10)
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