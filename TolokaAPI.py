from os import truncate
from re import X
import requests
import json

#Проект 61771
#архивный пул project/61771/pool/824431



def clonePool(poolNum,key,sandbox):
    '''
    Клоникование пула по его номеру. 
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.post(host+"/api/v1/pools/"+str(poolNum)+"/clone", headers=header)
    ss= json.loads(resp.text)
    return ss


def getPoolParams(poolNum,key,sandbox):
    '''
    Получение параметров пула по его номеру
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.get(host+"/api/v1/pools/"+str(poolNum), headers=header)
    ss= json.loads(resp.text)
    return ss

def createPool(poolparams,key,sandbox):
    '''
    Создание пула с параметрами, возвращает созданный пул. 
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key),'Content-Type': 'application/JSON'}
    
    resp = requests.post(host+"/api/v1/pools/", headers=header,data=json.dumps(poolparams))
    ss= json.loads(resp.text)
    return ss

def openPool(poolNum,key,sandbox):
    '''
    Открытие пула с параметрами, возвращает созданный пул. 
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.post(host+"/api/v1/pools/"+str(poolNum)+"/open", headers=header)
    ss= json.loads(resp.text)
    return ss

def closePool(poolNum,key,sandbox):
    '''
    Закрытие пула с параметрами, возвращает созданный пул. 
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.post(host+"/api/v1/pools/"+str(poolNum)+"/close", headers=header)
    ss= json.loads(resp.text)
    return ss

def GetResults(poolNum,key,sandbox):
    '''
    Получение результатов работы (ДОБАВЛЕНА СПЕЦИФИКА AIR)
        poolNum = номер пула из строки браузера, 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.get(host+"/api/v1/assignments?pool_id="+str(poolNum), headers=header)
    ss= json.loads(resp.text)
    result={}
    for x in ss['items']:
        for t in range(len(x['tasks'])):
            url= str(x['tasks'][t]['input_values']['url']).replace("https://storage.yandexcloud.net/bpla-photo-out/","")
            res= x['solutions'][t]['output_values']['result']
            if url not in result:
                result[url]=0
            if res is True:
                result[url]=result[url]+1
            else:
                result[url]=result[url]-1

    return result



def setPoolPriority(poolNum,value,key,sandbox):
    '''
    Установка приоритета пула 
        poolNum = номер пула из строки браузера,
        value = значение приоритета от 0 до 100 
        key = OAuth токен
        sandbox = Песочница или нет
    '''
    priorData= {
   "priority": value
        }  
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.patch(host+"/api/v1/pools/"+str(poolNum), headers=header,data=json.dumps(priorData))
    ss= json.loads(resp.text)
    return ss

def getTaskSuiteList(poolNum,key,sandbox):
    '''
    Получить страницы заданий из пула
    poolNum = номер пула из строки браузера,
    key = OAuth токен
    sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key)}
    resp = requests.get(host+"/api/v1/task-suites?pool_id="+str(poolNum), headers=header)
    ss= json.loads(resp.text)
    return ss


def CreateTaskSuit(TaskSuite,key,sandbox):
    '''
    Создание и загрузка списка страниц заданий
    TaskSuite = страницы заданий,
    key = OAuth токен
    sandbox = Песочница или нет
    '''
    if sandbox is True:
        host = "https://sandbox.toloka.yandex.ru"
    else:
        host = "https://toloka.yandex.ru"
    header = {'Authorization': 'OAuth {}'.format(key),'Content-Type': 'application/JSON'}
    
    resp = requests.post(host+"/api/v1/task-suites?async_mode=false&allow_defaults=true&skip_invalid_items=true", headers=header,data=json.dumps(TaskSuite))
    ss= json.loads(resp.text)
    return ss


def GenerateTaskPages(pool_id,overlap,kolInPage, URLS):
    '''
    Создание объекта TaskSuite для LIZAALERT_AIR из массива ссылок
    pool_id = номер пула полученый при создании нового пула,
    overlap = перекрытие
    kolInPage = количество заданий на странице
    URLS = массив ссылок
    '''
    TaskPages=[]
    ostatok= len(URLS)%10
    for x in range(int(len(URLS)/10)):
        tasks=[]
        OneTaskPage={"pool_id":pool_id,"overlap":overlap,"tasks":[]}
        for y in range(kolInPage):
            oneurl={'url':URLS[x*kolInPage+y]}
            onetask={'pool_id':pool_id,'input_values':{'url':URLS[x*kolInPage+y]}}
            tasks.append(onetask)
        OneTaskPage["tasks"]= tasks
        TaskPages.append(OneTaskPage)
    d= int(len(URLS)/10)*10
    tasks=[]
    OneTaskPage={"pool_id":pool_id,"overlap":overlap,"tasks":[]}
    for y in range(ostatok):
        oneurl={'url':URLS[x*kolInPage+y]}
        onetask={'pool_id':pool_id,'input_values':{'url':URLS[d+y]}}
        tasks.append(onetask)
    OneTaskPage["tasks"]= tasks
    TaskPages.append(OneTaskPage)
    return TaskPages

