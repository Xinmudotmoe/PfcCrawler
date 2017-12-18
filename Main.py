# coding=utf-8
import MyGet
import Myparser
import sys
import Utils
import urllib2
Rpath = sys.argv[0][:sys.argv[0].rfind("/")]
log = open("log.txt", 'w+',0)


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

    ##LiFo
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

    def ReadH(self, URL):
        # v1.1 修复了不能打开中文网址的bug
        NowUrl = URL
        Getting = MyGet.Getting(NowUrl.decode('utf-8').encode('gbk'), self.Rurl)
        Getting.LoadNow()
        Getting.save(Utils.getFilePath(Getting.get_url()))
        self.putSome(Getting.get_href())
        log.write(' '.join(("T", Getting.get_url(), str(Getting.code), str(Getting.types), "\n")))

    def run(self):
        while True:
            NextUrl = self.get()
            if isinstance(NextUrl, None.__class__):
                return

            try:
                self.ReadH(NextUrl)
            except urllib2.HTTPError:  # 获取现阶段的Bug
                log.write(' '.join(("E", str(NextUrl), "\n")))


if __name__ == "__main__":
    #WhatFuck = PaPa("http://118.190.20.36:80/Awebsite/Index.aspx")
    WhatFuck = PaPa("https://office.qq.com/index.html")
    WhatFuck.run()
    log.close()
