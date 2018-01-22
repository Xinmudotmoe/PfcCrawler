# coding=utf-8
import re
from HTMLParser import HTMLParser, HTMLParseError
import urlparse
h_url_re = re.compile('href ?= ?"([^"]+)"', re.I)  # 额外的空格是为了防止写花盆语言的灵魂代码工程师的灵魂花盆
r_url_re = re.compile('src ?= ?"([^"]+)"', re.I)  # 同上 Fixme:但还没有写GetSrcInele函数 Todo 临时压入了GetHref
R_url_re = re.compile('https?:\\/\\/[^\\/]+\\/', re.I)  # 解析域名
T_url_re = re.compile('[^.]\\.\\/')


def get_allurl(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return h_url_re.findall(data)


def get_allres(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return r_url_re.findall(data)


def Url_OA(url, Rurl):
    """
    @:param url:str host:str
    @:return str
    """

    if "://" in url:  # FIXME 猜测会出错
        Aurl = url
    elif url[0] == '/':
        TT = Rurl.find("/", 8)
        Aurl = ''.join((Rurl[:Rurl.find("/", 8)] if TT != -1 else Rurl, url))
    else:
        Aurl = ''.join((Rurl[:Rurl.rfind("/") + 1], url))

    A = re.sub("\.\.\/", "*-/", Aurl)  # 把../替换为*-
    A = re.sub("\.\/", "", A)  # 清除 ./

    Tt = A.find("*-/")  # FIXME:需要重写的代码 因为难看
    while Tt != -1:  # 清除../
        A = ''.join((A[:A.rfind("/", 0, Tt - 1)], A[Tt + 2:]))
        Tt = A.find("*-/")
    # Todo 网址里的\#号不知道是不是应该去掉 反正我去掉了
    TTTT = A.find("#")
    if TTTT != -1:
        A = A[:TTTT]
    # FIXME 需要适当增加index.html 也可能在MyGet.Getting.get_url就可以解决
    return A


class H_Parser(object, HTMLParser):
    src_href = set()
    Rurl = ""
    Host = ""
    Port = ""

    def __init__(self, Rurl):
        HTMLParser.__init__(self)
        self.src_href = set()
        self.Rurl = Rurl

    def feed(self, data):
        da = data
        super(H_Parser, self).feed(da)

    def handle_starttag(self, tag, attrs):
        # HTMLParser.HTMLParser会这样调用handle_starttag方法
        # <A HREF="https://www.cwi.nl/">                            ↓
        # handle_starttag('a', [('href', 'https://www.cwi.nl/')])
        #TODO: 需要地址筛选处理函数
        for i in attrs:
            if isinstance(i[0], str):
                if i[0] in ("href", "src", "HREF", "SRC"):
                    url = urlparse.urljoin(self.Rurl, i[1])
                    # 去除网页地址中的锚点
                    p = url.rfind("#")
                    if p!=-1:
                        url=url[:p]
                    self.src_href.add(url)
