import time

import pyexiv2
# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
from pyexiv2 import Image
import os
import shutil
import exifread

# PNG 图片使用 modify_exif 修改无效（exifread 无法读取到，上传到一刻时间也不对）

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            process_file(file_name)


def move_file(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))

def move_to_month_dir(path):
    time = get_image_time(path)
    if len(time) == 0:
        print("error time")
    else:
        print("时间：", time)
        month_time = time[0:7]
        month = month_time.replace(":", "-")
        month_dir = edit_time_path + month + "/"
        move_file(path, month_dir)

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

def process_file(path):
    if isPic(path):
        time = get_image_time(path)
        # 强制修改时间
        time = ""
        if len(time) == 0:
            # 修改时间并复制到对应的月份文件夹
            global edit_time
            try:
                test = Image(path)
                print("modify_time", edit_time)
                test.modify_exif({'Exif.Photo.DateTimeOriginal': edit_time})
                move_to_month_dir(path)
                # edit_time 转换成时间戳
                edit_time = update_edit_time(edit_time)
                # +1
                # 转化成时间字符串
            except Exception as e:
                print(e)
        else:
            move_to_month_dir(path)
    elif path.endswith(".MOV") \
            or path.endswith(".mp4") \
            or path.endswith(".MP4") \
            or path.endswith(".mov"):
        print("video")
    else:
        print("error file")


def get_image_time(path):
    time = ""
    if isPic(path):
        f = open(path, 'rb')
        tags = exifread.process_file(f)
        # 2020:10:11 09:42:31
        time = str(tags.get('EXIF DateTimeOriginal', ""))
    return time

dir_path = "/Users/yazhi/Documents/11_edit_backup/normal_image/2016-06"
# 修改后赋值到该目录下
edit_time_path = "/Users/yazhi/Documents/11_edit_backup/origin/"
# edit_time = "2019:11:17 13:17:28" #婚礼
# edit_time = "2017:06:17 11:17:28" #辅导君烧烤
edit_time = "2015:06:08 13:45:40"
# edit_time = "2021:11:19 21:30:00" # 迪士尼
# edit_time = "2020:12:16 19:55:00" # 哈尔滨


# 将 dir_path 目录里的所有照片都修改为 edit_time 时间（秒数会自增，保证时间不重复）
# 不支持 HEIC
if __name__ == '__main__':
    if os.path.isdir(dir_path):
        scan_dir(dir_path)
    else:
        try:
            test = Image(dir_path)
            print("modify_time", edit_time)
            test.modify_exif({'Exif.Photo.DateTimeOriginal': edit_time})
        except Exception as e:
            print(e)
