import proxy
import asyncio
import pdb
import aiohttp
import logging as log
from logging import info as printf
from conf import get_json_conf
from aiohttp_proxy import ProxyConnector, ProxyType

async def GetHtml(url, params=None, referer='', proxy=None, timeout=5):
    conf = get_json_conf()
    headers = {
            'User-Agent':conf['http']['user_agent'],
            "Referer":referer
    }
    connector = None
    if proxy is not None:
        connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.get(url,
                                   params=params,
                                   headers=headers,
                                   timeout=timeout) as resp:
                if resp.status == 200:
                    html =  await resp.text()
                    return {'url':url, 'resp':html}
                else:
                    printf("check status_code error:%d", resp.status)
                    return
        except asyncio.TimeoutError:
            # f是格式化, f-string
            printf(f"request {url} timeout proxy {proxy}")
            return
        except Exception as exc:
            printf(str(exc)+ " " + proxy)
            return

async def GetHtmlWithProxy(url, referer='', params=None, timeout=3):
    for i in range(5):
        _proxy = proxy.GetProxy()
        if _proxy is None:
            printf("get proxy error")
            return None
        proxy.SetUsed(_proxy)
        proxy_url = _proxy['type'] + '://'+_proxy['host']+':'+str(_proxy['port'])
        resp = await GetHtml(url, params, referer, proxy_url, timeout)
        if resp is not None:
            proxy.SetUnused(_proxy)
            break
        else:
            pass
    return resp

async def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    printf("main")
    await proxy.Init()
    resp = await GetHtmlWithProxy("http://www.baidu.com")
    print(resp)

if __name__ == '__main__':
    asyncio.run(main())
    
