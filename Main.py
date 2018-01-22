# coding=utf-8
import sys
import time
import urllib2

from Log import Log
import Utils
import MyGet
import Myparser
import urlparse
import threading

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
    lite_href = {}

    def __init__(self, url):
        self.Rurl = url
        self.OverUrl = []
        self.NextUrl = {url}
        self.ResourceUrl = []
        self.RpA = urlparse.urlparse(url)
        self.RootURL = self.RpA.netloc
        self.Host = self.RpA.hostname
        self.post = self.RpA.port if not isinstance(self.RpA.port, None.__class__) else 80
        self.lite_href = {}  # TODO

    ##like LiFo
    def put(self, url):
        if url in self.NextUrl or url in self.OverUrl:
            return
        pA = urlparse.urlparse(url)
        if pA.hostname != self.RpA.hostname:
            return
        # #端口分析
        # if (pA.port if isinstance(pA.port, None.__class__) else 80) != self.post:
        #    return

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

    def delNeUrl(self, url):  # 极大可能引发异常的方法
        self.NextUrl.remove(url)
        self.OverUrl.append(url)
        pass

    def ReadH(self, URL):
        # v1.1 修复了不能打开中文网址的bug
        _NowUrl = URL
        Getting = MyGet.Getting(_NowUrl.decode('utf-8').encode('gbk'), self.Rurl)
        Getting.LoadNow()
        NowUrl = Getting.get_url()
        Getting.save(Utils.getFilePath(NowUrl))
        if NowUrl != _NowUrl:
            Log.put_refresh(_NowUrl, NowUrl)
            if NowUrl in self.NextUrl:
                self.delNeUrl(NowUrl)
            elif NowUrl in self.OverUrl:
                return
        href = Getting.get_href()
        Log.put_hraf(_NowUrl, href)
        self.putSome(href)
        Log.put_Get_log(True, NowUrl, Getting.code, Getting.types)

    def run(self):
        while True:
            NextUrl = self.get()
            if isinstance(NextUrl, None.__class__):
                return
            if not debug:
                try:
                    self.ReadH(NextUrl)
                except urllib2.HTTPError, urllib2.URLError:  # 获取现阶段的Bug
                    Log.put_Get_log(False, NextUrl, None, None)
            else:
                self.ReadH(NextUrl)


class PPAP(PaPa):
    threads = 1
    pool = []

    class AThread(threading.Thread):
        func = None
        args = tuple()
        ret = None
        ID = 0

        def __init__(self, func, args):
            threading.Thread.__init__(self)
            self.func = func
            self.args = args
            self.ret = None

        def run(self):
            self.ID = -1
            try:
                self.ret = self.func(*self.args)
            except Exception, e:
                print self.args, e.args, e.message
                self.ret = None
            self.ID = 1

        def get_ret(self):
            return self.ret

    def set_threads(self, num):
        self.threads = num

    @staticmethod
    def ReadH0(Rurl, URL):
        _NowUrl = URL
        Getting = MyGet.Getting(_NowUrl.decode('utf-8').encode('gbk'), Rurl)
        Getting.LoadNow()
        NowUrl = Getting.get_url()
        Getting.save(Utils.getFilePath(NowUrl))
        return NowUrl == _NowUrl, _NowUrl, NowUrl, Getting.get_href(), Getting.code, Getting.types

    def ReadH1(self, isEqual, _OldUrl, NowUrl, href, code, types):
        if not isEqual:
            Log.put_refresh(_OldUrl, NowUrl)
            if NowUrl in self.NextUrl:
                self.delNeUrl(NowUrl)
            elif NowUrl in self.OverUrl:
                return
        Log.put_hraf(_OldUrl, href)
        self.putSome(href)
        Log.put_Get_log(True, NowUrl, code, types)

    def NewGet(self, url):
        _tmp = PPAP.AThread(PPAP.ReadH0, (self.Rurl, url))
        self.pool.append(_tmp)
        _tmp.start()

    def run(self):
        while True:
            while len(self.pool) <= self.threads:
                url = self.get()
                if isinstance(url, None.__class__):
                    break
                self.NewGet(url)
            if len(self.pool) == 0:
                break
            time.sleep(1)
            _o_pool = []
            _r_pool = []
            for i in self.pool:
                if i.ID == 1:
                    _o_pool.append(i)
                else:
                    _r_pool.append(i)
            self.pool = _r_pool
            for i in _o_pool:
                ret = i.get_ret()
                if isinstance(ret, None.__class__):
                    continue
                idea, _NowUrl, NowUrl, href, code, types = ret
                if not idea:
                    Log.put_refresh(_NowUrl, NowUrl)
                    if NowUrl in self.NextUrl:
                        self.delNeUrl(NowUrl)
                    elif NowUrl in self.OverUrl:
                        return
                Log.put_hraf(_NowUrl, href)
                self.putSome(href)
                Log.put_Get_log(True, NowUrl, code, types)


if __name__ == "__main__":
    # WhatFuck = PPAP("http://118.190.20.36:80/Awebsite/Index.aspx")
    WhatFuck = PPAP("https://www.lua.org/index.html")
    WhatFuck.run()
    Log.save()
