# coding=utf-8
import os
import re
from Myparser import R_url_re
rSub = re.compile("\\\\|\\/")
uHSub = re.compile("([a-zA-Z0-9]\\.)+[a-zA-Z0-9]+")


def getFilePath(Url, Root): # TODO:0.0.0.0:0 会出错 因为\:不能用作名字 下个版本修复
    """
    @:param Url:str Root:str
    @:rtype str
    """
    WSp = os.getcwd()  # WorkSpace
    # Host Space ###Start
    Tc = R_url_re.search(Url).group()
    Rc = ""
    Rc = Root if isinstance(Tc, None.__class__) else Tc
    Rc = Rc[8 if Rc[4] == 's' else 7:-1]
    # Host Space ###End
    # Dict Space ###Start
    Ds = Url[R_url_re.search(Url).end():Url.rfind('/')]
    """:type : str"""
    # Dict Space ###end
    # HaHaHa
    Dic = "\\".join((WSp, Rc, Ds))
    Dic = rSub.sub("$", Dic).split("$")
    Dir = ("/" if "/" in WSp else "\\").join(Dic)
    # Dir Space Over Yee

    # FileName Red Start
    Tn = Url[Url.rfind("/")+1:]
    if len(Tn) == 0:
        Tn = "index.html"
    Tn = re.sub("\?", "$", Tn)
    DicProFuc(Dic)
    return ("/" if "/" in WSp else "\\").join((Dir, Tn))


def DicProFuc(dL):
    """
    :param dL:[str,]
    :return:None
    """
    Cw = os.getcwd()
    C = ''.join((dL.pop(0), '\\'if '\\'in Cw else '/'))
    for sTr in dL:
        C = ('\\'if '\\'in Cw else '/').join((C,sTr))
        if not os.path.exists(C):
            os.mkdir(C)


