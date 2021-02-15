#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import logging as log
from logging import info as printf

def main():
    log.basicConfig(level=log.INFO, format='[%(filename)s:%(lineno)d] %(message)s')
    printf("start")

if __name__ == '__main__':
    main()
