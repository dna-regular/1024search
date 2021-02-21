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
        connector = ProxyConnector.from_url(proxy['url'])
    async with aiohttp.ClientSession(connector=connector) as session:
        ret = {'url':url, 'proxy':proxy, 'success':False}
        try:
            async with session.get(url,
                                   params=params,
                                   headers=headers,
                                   timeout=timeout) as resp:
                if resp.status == 200:
                    html =  await resp.read()
                    ret['resp'] = html
                    ret['success'] = True
                    return ret 
                else:
                    printf("err:%d url:%s proxy:%s", resp.status, url, proxy)
                    ret['reason'] = str(resp.status)
                    return ret 
        except asyncio.TimeoutError:
            # f是格式化, f-string
            printf(f"request {url} timeout proxy {proxy}")
            ret['reason'] = 'timeout'
            return ret
        except Exception as exc:
            printf(type(exc))
            printf(str(exc)+ " url:" + url + "proxy" + proxy)
            ret['reason'] = str(exc)
            return ret

async def GetHtmlWithProxy(url, referer='', params=None, timeout=3):
    _proxy = proxy.GetProxy()
    if _proxy is None:
        printf("get proxy error")
        return None
    proxy.SetUsed(_proxy)
    resp = await GetHtml(url, params, referer, _proxy, timeout)
    return resp

async def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    printf("main")
    await proxy.Init()
    resp = await GetHtmlWithProxy("http://www.baidu.com")
    print(resp)

if __name__ == '__main__':
    asyncio.run(main())
    
