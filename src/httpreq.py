import proxy
import asyncio
import aiohttp
import logging as log
from logging import info as printf
from conf import get_json_conf
from aiohttp_socks import ProxyConnector

async def GetHtml(url, params=None, referer=None, proxy=None, timeout=5):
    conf = get_json_conf()
    headers = {
            'User-Agent':conf['http']['user_agent'],
            "Referer":referer
    }
    connector = None
    if proxy is not None:
        connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, 
                               params=params, 
                               headers=headers, 
                               timeout=timeout) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                printf("check status_code error:%d", resp.status_code)
                return None

async def GetHtmlWithProxy(url, referer=None, params=None, timeout=10):
    for i in range(5):
        _proxy = proxy.GetProxy()
        if _proxy is None:
            printf("get proxy error")
            return None
        proxy.SetUsed(_proxy)
        proxy_url = _proxy['type'] + '://'+_proxy['host']+':'+str(_proxy['port'])
        proxies = {_proxy['type']: proxy_url}
        resp = await GetHtml(url, params, referer, proxy_url, timeout)
        if resp is not None:
            proxy.SetUnused(_proxy)
            break
        else:
            pass
    return resp

async def main():
    await proxy.Init()
    await GetHtmlWithProxy("http://www.baidu.com")
    print(resp)

if __name__ == '__main__':
    asyncio.run(main())
    
