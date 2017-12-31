# coding=utf-8
import sys
import urllib2

from Log import Log
import Utils
import MyGet
import Myparser

Rpath = sys.argv[0][:sys.argv[0].rfind("/")]

debug = False

class PaPa:
    # v1 初版
    # v1.1 没有修改
    OverUrl = []
    NextUrl = set()
    ResourceUrl = []
    Rurl = ''
    RootURL = ''

    def __init__(self, url):
        self.Rurl = url
        self.OverUrl = []
        self.NextUrl = {url}
        self.ResourceUrl = []
        self.RootURL = Myparser.R_url_re.findall(self.Rurl)[0]

    ##like LiFo
    def put(self, url):
        if url in self.NextUrl or url in self.OverUrl:
            return
        self.NextUrl.add(url)

    def putSome(self, List):
        for i in List:
            self.put(i)

    def get(self):
        rel = None
        if len(self.NextUrl) == 0:
            return rel
        rel = self.NextUrl.pop()
        self.OverUrl.append(rel)
        return rel

    def delNeUrl(self,url): # 极大可能引发异常的方法
        self.NextUrl.remove(url)
        self.OverUrl.append(url)
        pass

    def ReadH(self, URL):
        # v1.1 修复了不能打开中文网址的bug
        _NowUrl = URL
        Getting = MyGet.Getting(_NowUrl.decode('utf-8').encode('gbk'), self.Rurl)
        Getting.LoadNow()
        Getting.save(Utils.getFilePath(Getting.get_url()))
        NowUrl = Getting.get_url()
        if NowUrl != _NowUrl:
            Log.put_refresh(_NowUrl, NowUrl)
            if NowUrl in self.NextUrl:
                self.delNeUrl(NowUrl)
            elif NowUrl in self.OverUrl:
                return
        href = Getting.get_href()
        Log.put_hraf(_NowUrl, href)
        self.putSome(href)
        Log.put_Get_log(True,NowUrl, Getting.code,Getting.types)

    def run(self):
        while True:
            NextUrl = self.get()
            if isinstance(NextUrl, None.__class__):
                return
            if not debug:
                try:
                    self.ReadH(NextUrl)
                except urllib2.HTTPError,urllib2.URLError:  # 获取现阶段的Bug
                    Log.put_Get_log(False,NextUrl,None,None)
            else:
                self.ReadH(NextUrl)

if __name__ == "__main__":
    WhatFuck = PaPa("http://118.190.20.36:80/Awebsite/Index.aspx")
    #WhatFuck = PaPa("http://www.lua.org/index.html")
    WhatFuck.run()
    Log.save()