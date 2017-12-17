# coding=utf-8
import urllib2
import sys
import Myparser
import Utils
Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '
                  'Safari/537.36 '
}


class Getting:
    url = ''
    hx = ''
    RefUrl = ''
    types = ''
    r=''#Debug临时放在这
    def __init__(self, url, RefUrl = None):
        self.url = url
        self.RefUrl = url if isinstance(RefUrl, None.__class__) else RefUrl

    def LoadNow(self):
        req = urllib2.Request(self.url, headers=Headers)
        req.add_header('Referer', self.RefUrl.__repr__())
        self.r = urllib2.urlopen(req)
        self.hx = self.r.read()
        self.url = self.r.geturl()
        self.types = self.r.info().gettype()

    def get(self):
        return self.hx

    def get_href(self):
        return Myparser.GetHrefInele(self.hx, self.url)

    def get_url(self):
        return self.url

    def save(self, path):
        File = open(path, "wb")
        File.write(self.hx)
        File.close()


if __name__ == '__main__':
    # TODO: 没写完呢 千万别运行到这里 没用的
    raise Exception
    arc = sys.argv[1:]
    if len(arc) == 0:
        print("Error :argv is 0")
        sys.exit()
    elif len(arc) == 2:
        D = Getting(arc[1], arc[0])
    elif len(arc) == 1:
        D = Getting(*arc)
    D.LoadNow()
    D.get()  # ???????????
