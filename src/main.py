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

def callback(task):
    global err_cnt
    ret = task.result()
    _proxy = ret['proxy']
    url = ret['url']
    proxy.SetUnused(_proxy)
    if not ret['success'] and retry_cnt[url] <= 3:
        new_task = asyncio.create_task(httpreq.GetHtmlWithProxy(url))
        new_task.add_done_callback(callback)
        tasks.append(new_task)
        retry_cnt[url] = retry_cnt[url] + 1
        proxy.IncFailCnt(_proxy)
        return
    resp = str(ret['resp'], encoding='gbk')
    if keyword in resp:
        result_urls.append(ret['url'])

async def start(conf):
    for i in range(100):
        url = conf['http']['url'] + str(i)
        task = asyncio.create_task(httpreq.GetHtmlWithProxy(url))
        task.add_done_callback(callback)
        tasks.append(task)
    printf("fire tasks done")
    for task in tasks:
        await task


async def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    await proxy.Init()
    conf = get_json_conf()
    printf("start")
    await start(conf)

if __name__ == '__main__':
    keyword = sys.argv[1]
    asyncio.run(main())
    print(result_urls)
    printf("err count: %d", err_cnt)
