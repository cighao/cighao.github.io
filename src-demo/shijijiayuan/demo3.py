# -*- coding: UTF-8 -*-
import net.req
import requests
import dao.savedb
from multiprocessing.dummy import Pool as ThreadPool
import re


if __name__ == '__main__':
    # 登录
    session = requests.session()
    login_data = {'name': 'sjjy_a@sina.com', 'password': 'tobeyourself1314'}
    url = "https://passport.jiayuan.com/dologin.php?pre_url=http://usercp.jiayuan.com/"
    r = session.post(url, login_data)
    print(r.text)

    # 获取用户登录列表
    uid = []
    page = []
    for i in range(1, 50000):
        page.append([str(i), session])
    pool = ThreadPool(5)
    uid = pool.map(net.req.getUID, page)
    idlist = []
    for i in uid:
        for j in i:
            idlist.append(j)

    print(len(idlist))
    print(len(set(idlist)))

    #保存uid到数据库
    idlist = set(idlist)
    dao.savedb.insertUID(idlist)

    # 根据id找到用户信息
    uinfo = []
    for id in idlist:
        uinfo.append([id, session])
    pool = ThreadPool(5)
    uid = pool.map(net.req.getUserInfo, uinfo)


    # net.req.getUID(1, session)
    # net.req.getUserInfo("150071732", session)



