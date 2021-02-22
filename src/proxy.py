import ast
import asyncio
import httpreq
import time
from logging import info as printf

proxy_list = []
index = 0

async def Init():
   printf("init")
   await GetHttpsProxyList()

async def GetHttpsProxyList():
    proxies = await httpreq.GetHtml('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    if proxies is None:
        printf("get raw proxy list error")
        return None
    # 使用'\n' 切分字符串,得到一个list
    resp = str(proxies['resp'], encoding='utf-8')
    lines = resp.splitlines(False)
    for line in lines:
        # 只保留高密代理,https的一定是高密的
        if (line.find('https') > 0):
            try:
                proxy = ast.literal_eval(line)
                proxy['used'] = False
                proxy['url'] = proxy['type'] + '://' + \
                               proxy['host']+ ':' + str(proxy['port'])
                proxy['fail_cnt'] = 0
                proxy_list.append(proxy)
            except Exception as e:
                printf(str(e))
    printf("got %d proxies", len(proxy_list))

def GetUnusedProxy():
    global index
    for proxy in proxy_list[index:]:
        if (proxy['used'] == False):
            index = index + 1
            if index == len(proxy_list):
                index = 0
            return proxy
    return None

def GetProxy():
    for i in range(10):
        proxy = GetUnusedProxy()
        if (proxy):
            return proxy
        printf("no available proxy,sleep 1s to retry")
        time.sleep(1)
    printf("no available proxy, retry 10 times")
    return None

def SetUnused(proxy):
    proxy['used'] = False

def SetUsed(proxy):
    proxy['used'] = True

def RemoveProxy(proxy):
    proxy_list.remove(proxy)

def IncFailCnt(proxy):
    proxy['fail_cnt'] = proxy['fail_cnt'] + 1
    if proxy['fail_cnt'] >= 3:
       proxy_list.remove(proxy) 
