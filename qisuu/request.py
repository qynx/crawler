# 2019-08-11
import requests
import time


class Request():

    def __init__(self):
        '''
        考虑到session的特性 对同一host使用一个session
        可以极大提高下载速度
        '''
        self.session = requests.Session()

    def get(self, *args, **kw):
        kw["timeout"] = (5, 10)
        rsp = self.session.get(*args, **kw)
        return rsp

    def post(self, *args, **kw):
        kw["timeout"] = (5, 10)
        rsp = self.session.post(*args, **kw)
        return rsp