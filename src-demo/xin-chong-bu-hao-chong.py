# -*- coding:utf-8 -*-

# 爬取资源博客(250sb.cn)上的资源

from bs4 import BeautifulSoup
import requests
import re

headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Cache-Control':'max-age=0',
            'Cookie':'fsize=18; __cfduid=dddcd129a1f6a22f71e12bc894542d8a11492735435; cf_clearance=156fc38576e6dcdeb8a251df65b1a86de04b0348-1492735443-1800; UM_distinctid=15b8df746672a0-0b954b603e0d82-4e47052e-100200-15b8df74669318; CNZZDATA1260843977=1389977653-1492735449-null%7C1492736360'
        }

# 获取url集合
url="http://cuisiliu.com/book/6502/"
urllist={}
i=1;
base_num=2477550
for page in range(1,200):
    urllist[i] = url + str(base_num+i-1) + '.html'
    i=i+1;


r = requests.get(urllist[1])
print(urllist[1])
soup=BeautifulSoup(r.text,"html.parser")
a_tags = soup.find_all('h1')  #获取所有的h2标签

print(r.text)




