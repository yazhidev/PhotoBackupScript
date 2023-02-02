# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import shutil
import time
from pyexiv2 import Image
import get_time

def isPic(path):
    if path.endswith(".JPG") \
            or path.endswith(".jpg") \
            or path.endswith(".jpeg") \
            or path.endswith(".JPEG") \
            or path.endswith(".png") \
            or path.endswith(".PNG") \
            or path.endswith(".HEIC"):
        return True
    else:
        return False

def isPng(path):
    if path.endswith(".png") \
            or path.endswith(".PNG"):
        return True
    else:
        return False

def isVideo(path):
    if path.endswith(".MOV") \
            or path.endswith(".mp4") \
            or path.endswith(".MP4") \
            or path.endswith(".mov"):
        return True
    else:
        return False

def move_file(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))

def move_to_month_dir(path, dest_path):
    time = get_time.get_file_time(path)
    if len(time) == 0:
        print("error time")
    else:
        print("时间：", time)
        month_time = time[0:7]
        month = month_time.replace(":", "-")
        month_dir = dest_path + month + "/"
        move_file(path, month_dir)

def update_edit_time(now_time):
    # 先转换为时间数组
    time_array = time.strptime(now_time, "%Y:%m:%d %H:%M:%S")
    # 转换为时间戳
    time_stamp = int(time.mktime(time_array))
    print(time_stamp)
    # 自增
    time_stamp = time_stamp + 1
    # 转回时间字符串
    time_array = time.localtime(time_stamp)
    return time.strftime("%Y:%m:%d %H:%M:%S", time_array)

def change_file_time(path, edit_time):
    test = Image(path)
    print("modify_time", edit_time)
    test.modify_exif({'Exif.Photo.DateTimeOriginal': edit_time})