# -*- coding: UTF-8 -*-
import db.getConnect
import mysql.connector

def insertUID(uid):
    """向数据库中插入一组用户id"""
    connect = db.getConnect.getConn()
    cursor = connect.cursor()

    for id in uid:
        sql = "INSERT INTO UID VALUES(" + id + ")"
        try:
            cursor.execute(sql)
        except mysql.connector.Error as e:
            print('insert uid fails!{}'.format(e))
            continue
        connect.commit()
    connect.close


def insertUser(user):
    """向数据库中（user表）插入一组用户信息"""
    connect = db.getConnect.getConn()
    cursor = connect.cursor()
    sql = "INSERT INTO USER VALUES('" + user.uid + "','" +user.uage + "','" + user.uheight + "','" \
          + user.ueducation + "','" + user.usalary + "','" + user.uweight + "','" + user.uhouse \
          + "','" + user.uzodiac + "','" + user.ubtype + "','" + user.ustar + "','" + user.unation  \
          + "','" + user.ucar + "','" + user.uadress + "','" + user.uhousehold + "','" + user.unickname + "','" + user.ucharisma + "')"
    try:
        cursor.execute(sql)
    except mysql.connector.Error as e:
        print('insert user fails!{}'.format(e))
    connect.commit()
    connect.close

def insertObj(obj):
    """向数据库中（object表）插入一组择偶标准信息"""
    connect = db.getConnect.getConn()
    cursor = connect.cursor()
    sql = "INSERT INTO OBJECT VALUES('" + obj.uid + "','" +obj.age + "','" + obj.height + "','" \
          + obj.education + "','" + obj.nation + "','" + obj.adress + "')"
    try:
        cursor.execute(sql)
    except mysql.connector.Error as e:
        print('insert user fails!{}'.format(e))
        print(sql)
    connect.commit()
    connect.close