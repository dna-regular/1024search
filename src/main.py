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
urls = []
keyword = ''

def callback(task):
    global err_cnt
    ret = task.result()
    #printf(ret['url'])
    if not ret['success']:
        return
    resp = str(ret['resp'], encoding='gbk')
    if keyword in resp:
        urls.append(ret['url'])
        #printf(ret['url'])

tasks = []
async def start(conf):
    for i in range(100):
        url = conf['http']['url'] + str(i)
        task = asyncio.create_task(httpreq.GetHtmlWithProxy(url))
        task.add_done_callback(callback)
        tasks.append(task)
    printf("fire tasks done")
    for i in range(100):
        await tasks[i]


async def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    await proxy.Init()
    conf = get_json_conf()
    printf("start")
    await start(conf)

if __name__ == '__main__':
    keyword = sys.argv[1]
    asyncio.run(main())
    print(urls)
    printf("err count: %d", err_cnt)
