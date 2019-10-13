#coding: utf-8
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics

# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


# 图片路径, 裁剪压缩后覆盖原来图片
IMG_PATH = "img/"


def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "jpeg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
    # print new_list
    return new_list

def compress(choose, des_dir, src_dir, file_list):
    """压缩算法，img.thumbnail对图片进行压缩，
    
    参数
    -----------
    choose: str
            选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        img.save(des_dir + infile)

def compress_photo():
    '''调用压缩图片的函数
    '''
    src_dir, des_dir = IMG_PATH, IMG_PATH
    file_list_src = list_img_file(src_dir)
    compress('4', des_dir, src_dir, file_list_src)


def cut_photo():
    """裁剪算法
    
    ----------
    调用Graphics类中的裁剪算法，将img目录下的文件进行裁剪（裁剪成正方形）
    """
    src_dir = IMG_PATH
    
    # business logic
    file_list = list_img_file(src_dir)
    #print file_list
    if file_list:
        for infile in file_list:
            img = Image.open(src_dir+infile)
            Graphics(infile=src_dir+infile, outfile=src_dir + infile).cut_by_ratio()            
    else:
        pass


if __name__ == "__main__":
    # 图片保存在 img 目录下
    cut_photo()        # 裁剪图片 
    compress_photo()   # 压缩图片
    
    
    
    
