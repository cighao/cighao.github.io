# -*- coding: UTF-8 -*-
import requests
import re
import dao.savedb
import time
from vo import  user,object
from lxml import etree


def getUID(args):
    pageNum = args[0]
    session = args[1]
    time.sleep(0.5)
    url = 'http://search.jiayuan.com/v2/search_v2.php'
    payload = {'sex': 'f',
               'key': '',
               'stc': '23:1',
               'sn': 'default',
               'sv': '1',
               'p': pageNum,
               'f': 'select',
               'listStyle': 'bigPhoto',
               'pri_uid': 0,
               'jsversion': 'v5'}
    # headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    #            'Referer': 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=23:1&sn=default&sv=1&p=1&pt=67848&ft=off&f=select&mt=d',
    #            'X-Requested-With': 'XMLHttpRequest'}
    r = session.post(url, data=payload)
    pattern = '"userInfo":\[(.*?)\]'
    content = re.findall(pattern, r.text)[0]
    pattern = '"realUid":(\d+),'
    uidList = re.findall(pattern, content)
    return uidList

def getUserPage(uid, session):
    """得到用户主页的源码"""
    time.sleep(0.5)
    url = 'http://www.jiayuan.com/' + uid + '?fxly=search_v2'
    print("正在访问：" + url)
    headers = {'Referer': url,
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
               }
    r = session.post(url, headers=headers)
    if r.status_code != 200:
        print("get " + url + "failed")
        return ""
    return r.text


def getUserInfo(args):
    """获取用户信息"""
    uid = args[0]
    session = args[1]
    info = getUserPage(uid, session)
    if info == "":
        return
    selector = etree.HTML(info)
    # 用户信息
    unickname = selector.xpath('//div[@class="member_info_r yh"]/h4/text()')[0]
    ucharisma = selector.xpath('//div[@class="ml_ico"]/a/h6/text()')[0]
    content = selector.xpath('//h6[@class="member_name"]/text()')[0] + " "  # 27岁，未婚，来自湖南长沙
    uage = re.findall('(\d+)岁', content)[0]
    uadress = re.findall('来自(.*?) ', content)[0]
    infoList = selector.xpath('//ul[@class="member_info_list fn-clear"]/li/div[@class="fl pr"]/em/text()')

    # infoname = ['ueducation', 'uheight','ucar', 'usalary','uhouse'
    #             'uweight','ustar','unation','uzodiac','ubtype']

    for i in range(0, 10):
        if infoList[i] == '--':
            infoList[i] = ""
    u = user.User(uid, uage, infoList[1], infoList[0], infoList[3], infoList[5], infoList[4],
                  infoList[8], infoList[9], infoList[6], infoList[7], infoList[2], uadress, '', unickname, ucharisma)
    dao.savedb.insertUser(u)
    # 用户择偶信息
    # 用户择偶信息
    objinfo = selector.xpath('//div[@class="content_705"]/div[4]/div/ul/li/div/text()')
    o = object.Object(uid, objinfo[0], objinfo[1], objinfo[3], objinfo[2], objinfo[6])
    dao.savedb.insertObj(o)


def getCookies(filename):
    """获取本地Cookies"""
    f = open(filename, 'r')
    cookies = {}
    for line in f.readlines():
        key, value = line.split('=', 1)
        value = str(value).replace('\n', '')
        cookies[key] = value
    f.close()
    return cookies

