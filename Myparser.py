# coding=utf-8
import re

h_url_re = re.compile('href ?= ?"([^"]+)"')  # 额外的空格是为了防止写花盆语言的灵魂代码工程师的灵魂花盆
r_url_re = re.compile('src ?= ?"([^"]+)"')  # 同上 Fixme:但还没有写GetSrcInele函数 Todo 临时压入了GetHref
R_url_re = re.compile('https?:\\/\\/[^\\/]+\\/')  # 解析域名
T_url_re = re.compile('[^.]\\.\\/')

def get_allurl(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return h_url_re.findall(data)


def get_allres(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return r_url_re.findall(data)


def GetHrefInele(data, Turl):#TODO 急需更好的URL地址处理函数
    """
    @:param data:str Turl:str
    @:rtype [str,]
    """
    BigList = []
    TbList = []
    Td = h_url_re.findall(data)
    Td.extend(r_url_re.findall(data))
    Host = R_url_re.search(Turl).group()[:-1]   # 现在所处的Host
    Tl = set(Td)
    for i in Tl:
        if i.find("://") != -1:  # 如果成功找到的话 那么这个地址将收到抨击 必须证明此地址属于Host的此根 否则将被丢弃
            TbList.append(i)
        else:  # 如果没能找到的话 这个地址为相对地址 进行相对移动
            BigList.append(Url_OA(i, Turl))

########            if i[0] == "/":  # 表示指向根
########                BigList.append(''.join((Host, i)))
########            else:
########                TA = list(TL)
########                while True:
########                    if i[:3] == "../":
########                        TA.pop(-1)
########                        i = i[3:]
########                    else:
########                        TA.append(i)
########                        TA.insert(0, Host)
########                        BigList.append('/'.join(TA))
########                        break
    #TODO:丢弃吧 不想改 ->line:32
    return BigList

def Url_OA(url, Rurl):
    """
    @:param url:str host:str
    @:return str
    """

    if "://"in url:  # FIXME 猜测会出错
        Aurl=url
    elif url[0] == '/':
        TT=Rurl.find("/", 8)
        Aurl = ''.join((Rurl[:Rurl.find("/", 8)] if TT!=-1 else Rurl, url))
    else:
        Aurl = ''.join((Rurl[:Rurl.rfind("/")+1], url))

    A = re.sub("\.\.\/", "*-/", Aurl)  # 把../替换为*-
    A = re.sub("\.\/", "", A)  # 清除 ./

    Tt = A.find("*-/")  # FIXME:需要重写的代码 因为难看
    while Tt != -1:  # 清除../
        A = ''.join((A[:A.rfind("/", 0, Tt-1)], A[Tt+2:]))
        Tt = A.find("*-/")
    # Todo 网址里的\#号不知道是不是应该去掉 反正我去掉了
    TTTT = A.find("#")
    if TTTT != -1:
        A = A[:TTTT]
    #FIXME 需要适当增加index.html 也可能在MyGet.Getting.get_url就可以解决
    return A
