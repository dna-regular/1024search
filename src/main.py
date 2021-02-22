#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import sys
import proxy
import httpreq
import asyncio
import logging as log
from logging import info as printf
from conf import get_json_conf

err_cnt = 0
result_urls = []
keyword = ''
tasks = []
retry_cnt = {}
MAX_PAGES = 20
RETRY_MAX = 3

def callback(task):
    global err_cnt
    ret = task.result()
    _proxy = ret['proxy']
    url = ret['url']
    if not ret['success']:
        if retry_cnt[url] <= RETRY_MAX:
            new_task = asyncio.create_task(httpreq.GetHtmlWithProxy(url))
            new_task.add_done_callback(callback)
            tasks.append(new_task)
            retry_cnt[url] = retry_cnt[url] + 1
        proxy.SetUnused(_proxy)
        proxy.IncFailCnt(_proxy)
        return
    proxy.SetUnused(_proxy)
    printf('req url: %s success', url)
    resp = str(ret['resp'], encoding='gbk')
    if keyword in resp:
        result_urls.append(ret['url'])

async def start(conf):
    for i in range(MAX_PAGES):
        url = conf['http']['url'] + str(i)
        retry_cnt[url] = 0
        task = asyncio.create_task(httpreq.GetHtmlWithProxy(url))
        task.add_done_callback(callback)
        tasks.append(task)
    printf("fire tasks done")
    for task in tasks:
        await task

async def main():
    global err_cnt
    log.basicConfig(level=log.INFO, format='[ %(filename)s: %(lineno)d ] %(message)s')
    await proxy.Init()
    conf = get_json_conf()
    printf("start")
    await start(conf)
    for url, cnt in retry_cnt.items():
        if cnt > RETRY_MAX:
            printf("url: %s retry %d times still fail", url, cnt)
            err_cnt += 1

if __name__ == '__main__':
    keyword = sys.argv[1]
    asyncio.run(main())
    printf('results: ')
    for url in result_urls:
        print('\t' + url)
    printf("err count: %d", err_cnt)
