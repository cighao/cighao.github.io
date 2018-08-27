# -*- coding: UTF-8 -*-
class Object:
    """用户择偶信息"""
    def __init__(self, uid, age, height, education, nation, adress):
        self.uid = uid  # 用户id
        self.age = age  # 择偶要求：年龄
        self.height = height  # 身高
        self.education = education  # 学历
        self.nation = nation  # 名族
        self.adress = adress  # 居住地