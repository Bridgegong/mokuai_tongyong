# -*- coding: utf-8 -*-
# @Time    : 2018/5/23 13:58
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : KBoxBrUtils.py
# @Software: PyCharm
import json
from string import Template
import requests
import KBoxBrConfig
configCache = {}

def getConfigStringById( configId, params):
    if configCache.__contains__(configId)==False:
        configHtml = requests.get('http://192.168.1.152:8888/srs/dboxService/getHttpRequestConfig?id='+configId)
        configHtml.encoding = "utf-8"
        configCache[configId] = configHtml.text

    httpConfig = configCache[configId]
    # print("t:" + httpConfig)
    jsonTemp = Template(httpConfig)
    httpConfig = jsonTemp.substitute(params)
    # print("s:"+httpConfig)
    configJson = json.loads(httpConfig)
    return json.loads(configJson['HTTP_CONFIG'])

def request(configId, params, data):
    configJson = getConfigStringById(configId, params)
    # print(configJson)
    ___url = configJson['url']['raw']
    ___headers = {}

    if configJson['header'] != None:
        for thisKeyAndValue in configJson['header']:
            ___headers[thisKeyAndValue['key']] = thisKeyAndValue['value']

    if configJson['method'] == 'GET':
        # print("[URL]"+___url)
        html = requests.get(___url, headers=___headers)
        # print(html)
        html.encoding = html.apparent_encoding if params == None else (html.apparent_encoding if params.__contains__('charset') == False else params['charset'])
        return html.text
    else:
        ___data = {} if data == None else data
        if configJson['body'] != None:
            formData = configJson['body']['formdata']
            for thisKeyAndValue in formData :
                ___data[thisKeyAndValue['key']] = thisKeyAndValue['value']
        html = requests.post(___url, data=___data, headers=___headers)
        # print(html.apparent_encoding)
        html.encoding = html.apparent_encoding if params == None else (html.apparent_encoding if params['charset'] == None else params['charset'])
        return html.text

def saveToDB(tableName,objectArray):
    __url = KBoxBrConfig.statusServer + "/srs/KBoxBrDBAPI/insert?appId=" + KBoxBrConfig.appId + "&instanceId=" + KBoxBrConfig.instanceId
    __data_json = json.dumps(objectArray)
    html = requests.post(__url, data={
        'table':tableName,
        'values':__data_json
    })
    return json.loads(html.text);


def getCache(url):
    __url = KBoxBrConfig.cacheServer + "/srs/KBoxBrCacheService/getPrevSetTime"
    html = requests.post(__url, data={
        'key':url
    })

    return int(html.text);
def setCache(url):
    __url = KBoxBrConfig.cacheServer + "/srs/KBoxBrCacheService/setPrevSetTime"
    html = requests.post(__url, data={
        'key':url
    })
    return html.text.strip();

def getTask(taskType):
    __url = KBoxBrConfig.cacheServer + "/srs/KBoxBrCacheService/getTask?taskType=" + taskType
    html = requests.get(__url)
    return html.text

def removeTask(taskType,taskString):
    __url = KBoxBrConfig.cacheServer + "/srs/KBoxBrCacheService/removeTask?taskType=" + taskType
    html = requests.post(__url, data={
        'task':taskString
    })
    return html.text.strip();