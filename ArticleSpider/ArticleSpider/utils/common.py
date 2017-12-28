# -*- coding:utf-8 -*- 
__author__ = 'John 2017/12/27 12:07'
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()