#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import html2text
import requests


if __name__ == '__main__':
    if len(sys.argv)<=1:
        usage = """
使用方法:
    1. python html2txt.py <url> [start_str] [end_str]
    2. python html2txt.py <字符串>
"""
        print(usage)
        sys.exit(1)
    if sys.argv[1].startswith("http"):
        headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
            }
        resp = requests.get(sys.argv[1], headers=headers)
        if resp.status_code == 200:
            text = resp.text
            if "<body" in text:
                text = text[text.find("<body"):]
            start = 0
            end = len(text)
            if len(sys.argv)>2 and sys.argv[2]:
                start = text.find(sys.argv[2])
                while start>0 and text[start]!="<":
                    start -= 1

            if len(sys.argv)>3 and sys.argv[3]:
                end = text.find(sys.argv[3])

            print(html2text.html2text(text[start: end]))
        else:
            print("获取数据失败，status code:", resp.status_code)
    else:
        print(html2text.html2text(sys.argv[1]))

