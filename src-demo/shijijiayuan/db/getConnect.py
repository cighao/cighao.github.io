import mysql
from mysql import connector
# -*- coding: UTF-8 -*-


def getConn():
    """获取数据库连接"""
    user = 'root'
    pwd = ''
    host = '127.0.0.1'
    db = 'shijiejiayuan'
    charset = 'utf8'
    try:
        connect = mysql.connector.connect(user=user, password=pwd, host=host, database=db, charset=charset)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
        return None
    return connect
