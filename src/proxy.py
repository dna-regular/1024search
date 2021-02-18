import ast
import httpreq
import time
from logging import info as printf

proxy_list = []

def Init():
   GetHttpsProxyList()

def GetHttpsProxyList():
    proxies = http.GetHtml('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    if proxies is None:
        printf("get raw proxy list error")
        return None
    # 使用'\n' 切分字符串,得到一个list
    lines = proxies.splitlines(False)
    for line in lines:
        # 只保留高密代理,https的一定是高密的
        if (line.find('https') > 0):
            try:
                proxy = ast.literal_eval(line)
                proxy['used'] = False
                proxy_list.append(proxy)
            except Exception as e:
                printf(str(e))

def GetUnusedProxy():
    for proxy in proxy_list:
        if (proxy['used'] == False):
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
