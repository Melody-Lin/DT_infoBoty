#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
try:
    from intent import Loki_Credit_income
    from intent import Loki_Mortgage_Time
    from intent import Loki_Exp_Time
    from intent import Loki_Education
    from intent import Loki_Mortgage_type
    from intent import Loki_Probe
    from intent import Loki_Mortgage_Addr
    from intent import Loki_Mortgage_floorsize
    from intent import Loki_Credict_job
except:
    from .intent import Loki_Credit_income
    from .intent import Loki_Mortgage_Time
    from .intent import Loki_Exp_Time
    from .intent import Loki_Education
    from .intent import Loki_Mortgage_type
    from .intent import Loki_Probe
    from .intent import Loki_Mortgage_Addr
    from .intent import Loki_Mortgage_floorsize
    from .intent import Loki_Credict_job


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = ""
LOKI_KEY = ""
# ?????????????????????
# INTENT_FILTER = []        => ????????????????????? (??????)
# INTENT_FILTER = [intentN] => ????????? INTENT_FILTER ????????????
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST ???????????????????????? INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # Credit_income
                if lokiRst.getIntent(index, resultIndex) == "Credit_income":
                    resultDICT = Loki_Credit_income.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Mortgage_Time
                if lokiRst.getIntent(index, resultIndex) == "Mortgage_Time":
                    resultDICT = Loki_Mortgage_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Exp_Time
                if lokiRst.getIntent(index, resultIndex) == "Exp_Time":
                    resultDICT = Loki_Exp_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Education
                if lokiRst.getIntent(index, resultIndex) == "Education":
                    resultDICT = Loki_Education.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Mortgage_type
                if lokiRst.getIntent(index, resultIndex) == "Mortgage_type":
                    resultDICT = Loki_Mortgage_type.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Probe
                if lokiRst.getIntent(index, resultIndex) == "Probe":
                    resultDICT = Loki_Probe.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Mortgage_Addr
                if lokiRst.getIntent(index, resultIndex) == "Mortgage_Addr":
                    resultDICT = Loki_Mortgage_Addr.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Mortgage_floorsize
                if lokiRst.getIntent(index, resultIndex) == "Mortgage_floorsize":
                    resultDICT = Loki_Mortgage_floorsize.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Credict_job
                if lokiRst.getIntent(index, resultIndex) == "Credict_job":
                    resultDICT = Loki_Credict_job.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)


if __name__ == "__main__":
    ## Credit_income
    #print("[TEST] Credit_income")
    #inputLIST = ['100???','??????100???','?????????100???','?????????100???','?????????100???','?????????100??????']
    #testLoki(inputLIST, ['Credit_income'])
    #print("")

    ## Mortgage_Time
    #print("[TEST] Mortgage_Time")
    #inputLIST = ['????????????','????????????','???????????????']
    #testLoki(inputLIST, ['Mortgage_Time'])
    #print("")

    ## Exp_Time
    #print("[TEST] Exp_Time")
    #inputLIST = ['??????','????????????','???????????????','??????????????????','????????????????????????','???????????????????????????']
    #testLoki(inputLIST, ['Exp_Time'])
    #print("")

    ## Education
    #print("[TEST] Education")
    #inputLIST = ['????????????','??????????????????','?????????????????????','???????????????????????????','???????????????????????????']
    #testLoki(inputLIST, ['Education'])
    #print("")

    ## Mortgage_type
    #print("[TEST] Mortgage_type")
    #inputLIST = ['??????','??????','10?????????','????????????']
    #testLoki(inputLIST, ['Mortgage_type'])
    #print("")

    ## Probe
    #print("[TEST] Probe")
    #inputLIST = ['????????????','??????????????????','??????????????????','????????????????????????','??????????????????????????????','??????????????????????????????????????????']
    #testLoki(inputLIST, ['Probe'])
    #print("")

    ## Mortgage_Addr
    #print("[TEST] Mortgage_Addr")
    #inputLIST = ['?????????????????????????????????10???']
    #testLoki(inputLIST, ['Mortgage_Addr'])
    #print("")

    ## Mortgage_floorsize
    #print("[TEST] Mortgage_floorsize")
    #inputLIST = ['100???']
    #testLoki(inputLIST, ['Mortgage_floorsize'])
    #print("")

    ## Credict_job
    #print("[TEST] Credict_job")
    #inputLIST = ['???????????????','?????????????????????']
    #testLoki(inputLIST, ['Credict_job'])
    #print("")

    # ???????????????????????????
    inputLIST = ["?????????????????????", "??????????????????"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Result => {}".format(resultDICT))