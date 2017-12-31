# coding=utf-8
import urllib2
import sys
import Myparser
import Utils
import re

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 '
                  'Safari/537.36 '
}

UnH = ["application/octet-stream",
       "image/x-icon",
       "image/jpeg",
       "image/png",
       "video/quicktime",
       "text/plain",
       "application/pdf",
       "image/bmp",
       "application/msword",
       "image/gif",
       "application/gzip"]  # 无需进行识别的类型

AnH = ["text/html",
       "text/css",
       "application/x-javascript",
       "application/javascript",
       "application/xml",
       "application/rss+xml"]


class Getting:
    url = ''
    hx = ''
    RefUrl = ''
    types = ''
    r = ''  # Debug临时放在这
    code = 0

    def __init__(self, url, RefUrl = None):
        self.url = re.sub(' ', '%20', url)  # Fixme 暂且不知道有什么更好的修正方式
        self.RefUrl = url if isinstance(RefUrl, None.__class__) else RefUrl
        self.code = 0

    def LoadNow(self):
        req = urllib2.Request(self.url, headers=Headers)
        req.add_header('Referer', self.RefUrl.__repr__())
        self.r = urllib2.urlopen(req)
        self.url = self.r.geturl()
        self.hx = self.r.read()
        self.types = self.r.info().gettype()
        self.code = self.r.code

    def get(self):
        return self.hx

    def get_href(self):
        if self.types not in UnH and self.types not in AnH:  # Todo Debug用
            print "UnKnow Type", self.types
        return Myparser.GetHrefInele(self.hx, self.url) if self.types not in UnH else []

    def get_url(self):
        return self.url

    def save(self, path):
        File = open(path, "wb")
        File.write(self.hx)
        File.close()
