# coding=utf-8
# import sqlite3
import json
import sys
import pickle

class __interface_Log:
    def __init__(self):
        pass

    def put_log(self, *args):
        raise Exception("Bad Class")

    def put_Get_log(self, type, url, Status_Code, Content_Type):
        raise Exception("Bad Class")

    def put_refresh(self, source, target):
        raise Exception("Bad Class")

    def put_hraf(self, url, hraf):
        raise Exception("Bad Class")

    def save(self):
        raise Exception("Bad Class")


class _SqlToTxt_Log(__interface_Log):
    pass


class _Sql_Log(__interface_Log):
    pass


class _Json_Log(__interface_Log):
    data = {"GetLog": [], "refresh": {}, "hrah": {}}

    def __init__(self):
        self.data = {"GetLog": [], "refresh": {}, "hrah": {}}

    def put_log(self, *args):
        pass

    def put_Get_log(self, type, url, Status_Code, Content_Type):
        self.data["GetLog"].append((type, url, Status_Code, Content_Type))

    def put_refresh(self, source, target):
        self.data["refresh"][source] = target

    def put_hraf(self, url, hraf):
        self.data["hrah"][url] = hraf

    def save(self):
        return 0  # 会抛出异常
        log = open("Log.json", "wb")
        data = json.dumps(self.data)
        log.write(data)
        log.close()


Log = _Json_Log()
