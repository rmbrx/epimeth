#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import tomd # 等 tomd bug 修复后再用
import sys
import requests

from pyquery import PyQuery as pq

MARKDOWN = {
    'h1': "#",
    'h2': "##",
    'h3': "###",
    'h4': "####",
    'h5': "#####",
    'h6': "######",
    "blockquote": ">",
    "li": "-",
    "hr": "---",
    "p": "\n",
}

INLINE = {
    'em': ('*', '*'),
    'strong': ('**', '**'),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    "code": ('`', '`')
}

split_str = "++++++++++++++++++"

def convert(html=""):
    d = pq(html)

    d('head').remove()
    html = d.html()

    d = pq(html)
    for e in d('span'):
        inline_mark = pq(e).text()
        html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    for e in d('a'):
        if "http" in pq(e).attr('href'):
            inline_mark = f"[{pq(e).text()}]({pq(e).attr('href')})"
            html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    for e in d('thead'):
        inline_mark = pq(e).outer_html() + '|------' * (pq(e)('th').length - 1)
        html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    for e in d('th,td'):
        inline_mark = "|" + pq(e).text()
        html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    for e in d('pre'):
        inline_mark = "```" + split_str + pq(e).html() + split_str + "```" + split_str
        html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    selectors = ','.join(INLINE.keys())
    for e in d(selectors):
        inline_mark = INLINE.get(e.tag)[0] + pq(e).text() + INLINE.get(e.tag)[1]
        html = html.replace(str(pq(e)), inline_mark)

    d = pq(html)
    selectors = ','.join(MARKDOWN.keys())
    for e in d(selectors):
        inline_mark = split_str + MARKDOWN.get(e.tag) + " " + pq(e).text() + split_str
        html = html.replace(str(pq(e)), inline_mark)

    # img 要放到最后，否则就会被替换成空（这就是 tomd 的bug）
    d = pq(html)
    for e in d('img'):
        img_alt = pq(e).attr('alt') if pq(e).attr('alt') else ""
        img_src = pq(e).attr('src')
        if img_src.startswith("data:"):
            continue
        inline_mark = f"![{img_alt}]({pq(e).attr('src')})"
        html = html.replace(str(pq(e)), inline_mark)

    markdown = pq(html).text().replace(split_str, '\n')

    return markdown


if __name__ == '__main__':
    if len(sys.argv)<=1:
        usage = """
使用方法:
    1. python html2md.py <url> [start_str] [end_str]
    2. python html2md.py <字符串>
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

            # print(tomd.convert(text[start: end]))
            print(convert(text[start: end]))
        else:
            print("获取数据失败，status code:", resp.status_code)
    else:
        # print(tomd.convert(sys.argv[1]))
        print(convert(sys.argv[1]))
