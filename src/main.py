#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import proxy
import logging as log
from logging import info as printf
from conf import get_json_conf


def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    proxy.Init()
    conf = get_json_conf()
    printf("start")

if __name__ == '__main__':
    main()
