# -*- coding:utf-8 -*-

# 爬取资源博客(250sb.cn)上的资源

from bs4 import BeautifulSoup
import requests
import re

headers = {
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible MSIE 6.00 Windows NT 5.1 SV1)',
        }

# 获取url集合
url="http://250sb.ren/page/"
urllist={}
i=1;
for page in range(1,200):
    urllist[i] = url + str(page)
    i=i+1;


# 开始爬取数据
tmp_link={}  # 保存链接
text={}  # 保存说明
j=1;
for i in range(1,len(urllist)+1):
    r = requests.get(urllist[i])
    soup=BeautifulSoup(r.text,"html.parser")
    a_tags = soup.find_all('h2')  #获取所有的h2标签
    for tmp in a_tags:            #依次遍历
        tmp_link[j]=tmp.a.get("href")  #提取h2标签内部的a标签信息
        text[j]=tmp.a.text
        j=j+1
        
link={}  # 链接
pwd={}   # 密码
for i in range(1,len(text)+1):
    # 爬取密码
    r = requests.get(tmp_link[i])
    pat="解压密码：(.*?)\n"
    result = re.findall(pat,r.text)
    if(result!=[]):
        pwd[i]=result[0]
    else:
        pat="解压密码：(.*?)\n"
        result = re.findall(pat,r.text)
        if(result!=[]):
            pwd[i]=result[0]
        else:
            pwd[i]=""
    
    # 爬取百度云盘的分享链接
    pat='百度云盘：<a href="(.*?)"'
    result = re.findall(pat,r.text)
    if(result==[]):
        link[i]=""
        continue
    r=requests.get(result[0])
    pat='id="liajie" href="(.*?)"'
    result = re.findall(pat,r.text)
    if(result==[]):
        link[i]=""
        continue
    link[i]=result[0]

    # 获取分享文件的文件名
    s = requests.Session()
    #aaaa=link[i]+"#list/path=%2F"
    #aaaa="https://pan.baidu.com/s/1jHWxNRg#list/path=%2F"
    #print(aaaa)
    #r=s.get(aaaa,verify=False)
    #r.encoding="utf-8"
    #print(r.text)
    

# 保存数据
output=open("data.txt",'w',encoding='utf-8')
for i in range(1,len(pwd)+1):
    line = text[i] + '\t' + link[i] + '\t' + pwd[i] + '\n'
    output.write(line)
output.close()


    
