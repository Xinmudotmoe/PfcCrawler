# coding=utf-8
import re

h_url_re = re.compile('href ?= ?"([^"]+)"')  # 额外的空格是为了防止写花盆语言的灵魂代码工程师的灵魂花盆
r_url_re = re.compile('src ?= ?"([^"]+)"')  # 同上 Todo:但还没有写GetSrcInele函数
R_url_re = re.compile('https?:\\/\\/[^\\/]+\\/')  # 解析域名


def get_allurl(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return h_url_re.findall(data)


def get_allres(data):
    if not isinstance(data, str):
        data = ''.join(i for i in data)
    return r_url_re.findall(data)


def GetHrefInele(data, Turl):
    """
    @:param data:str Turl:str
    @:rtype [str,]
    """
    BigList = []
    TbList = []
    Host = R_url_re.search(Turl).group()[:-1]   # 现在所处的Host
    TL = Turl[len(Host):].split("/")[1:-1]
    Tl = set(h_url_re.findall(data))
    for i in Tl:
        if R_url_re.findall(i):  # 如果成功找到的话 那么这个地址将收到抨击 必须证明此地址属于Host的此根 否则将被丢弃
            TbList.append(i)
        else:  # 如果没能找到的话 这个地址为相对地址 进行相对移动
            if i[0] == "/":  # 表示指向根
                BigList.append(''.join((Host, i)))
            else:
                TA = list(TL)
                while True:
                    if i[:3] == "../":
                        TA.pop(-1)
                        i = i[3:]
                    else:
                        TA.append(i)
                        TA.insert(0,Host)
                        BigList.append('/'.join(TA))
                        break
    #TODO:丢弃吧 不想改 ->line:32
    return BigList
