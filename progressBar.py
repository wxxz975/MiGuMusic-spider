#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:Administrator
@file:progressBar_1.py
@time:2020/11/05
"""
import os
from time import time, sleep
from requests import get


def progressbar(url, path, delUnsuccess = False):
    """
    :param url:   下载地址
    :param path: 完整的路径名称
    :return: True 或者 False
    :delUnsuccess: 下载失败之后是否自动删除文件
    """
    start = time()  # 下载开始时间
    response = get(url, stream=True)
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    
    if content_size < 1024:
        print("\033[31m 获取下载文件失败... \033[0m")
        return False
    
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            with open(path, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                end = time()  # 下载结束时间
                print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
    except Exception as e:
        print('Error!' + e)
        return False
    
    finally:
        print("\033[32m Download complete... \033[0m")



if __name__ == "__main__":
    progressbar("http://218.205.239.34/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag=SQ&netType=00&copyrightId=0&contentId=600902000006889066&resourceType=E&channel=0","./music.mp3")


