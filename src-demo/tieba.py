#爬取百度贴吧内容

# -*- coding: utf-8 -*- 
import requests
import re
import os
import sys
import time
from bs4 import BeautifulSoup

pageNum = 10;  # 所有帖子总共10页
urlsFile = os.path.join(sys.path[0],'urls.txt');# 保存帖子url的本地路径
infoNum = 0; #有效信息的总条数
borthList = list();

# 获取所有帖子的url
def getUrls():
    if(os.path.exists(urlsFile)):
        return getUrlsFromFile();#如果本地存在数据直接从本地读取
    urlList = list();
    for i in range(1,pageNum):
        url = "http://date.jobbole.com/page/"+str(i)+"/?sort=latest";
        html = requests.get(url);
        pattern = "href=\"(.*?)\">.*?</a><label class=\"hide-on-480 small-domain-url\"></label>";
        result = re.findall(pattern,html.text);
        urlList = urlList + result
    saveUrls(urlList); #保存到本地
    return urlList;

#本地读取所有帖子的url
def getUrlsFromFile():
    urlList = list();
    f = open("urls.txt","r");
    for line in f.readlines():
        urlList.append(line);
    f.close();
    return urlList;

#将帖子url存入本地文件中
def saveUrls(urlList):
    f = open("urls.txt","w")
    f.write('%s' % '\n'.join(urlList));

#查询该帖子下的内容
def viewUrl(url):
    global infoNum;
    global borthList;
    result = "";
    html = requests.get(url);
    soup = BeautifulSoup(html.text,"lxml");
    info = soup.find("div",{"class":"p-entry"});
    info = str(info);
    pattern = "出生年月：(\d{4})";
    r = re.findall(pattern,info);
    if(len(r)>0 and (r[0]!="")):
        infoNum  = infoNum+ 1;
        if(r[0]=="1994" or r[0]=="1980"):
            print(url);
        borthList.append(r[0]);


if __name__=='__main__':
	#
	#

    
    
