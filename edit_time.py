import time

import pyexiv2
# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
from pyexiv2 import Image
import os
import shutil
import exifread

import get_time
import my_utils

# PNG 图片使用 modify_exif 修改无效（exifread 无法读取到，上传到一刻时间也不对）

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            process_file(file_name)

def process_file(path):
    if my_utils.isPic(path):
        time = get_time.get_file_time(path)
        # 强制修改时间
        time = ""
        if len(time) == 0:
            # 修改时间并复制到对应的月份文件夹
            global edit_time
            try:
                my_utils.change_file_time(path, edit_time)
                my_utils.move_to_month_dir(path, edit_time_path)
                # edit_time 转换成时间戳
                edit_time = my_utils.update_edit_time(edit_time)
                # +1
                # 转化成时间字符串
            except Exception as e:
                print(e)
        else:
            my_utils.move_to_month_dir(path, edit_time_path)
    elif path.endswith(".MOV") \
            or path.endswith(".mp4") \
            or path.endswith(".MP4") \
            or path.endswith(".mov"):
        print("video")
    else:
        print("error file")


dir_path = "/Users/yazhi/Documents/11_edit_backup/test/20230127-184318-IMG_0640.jpeg"
# 修改后复制到该目录下
edit_time_path = "/Users/yazhi/Documents/11_edit_backup/origin/"
# edit_time = "2019:11:17 13:17:28" #婚礼
# edit_time = "2017:06:17 11:17:28" #辅导君烧烤
edit_time = "2020:01:21 18:27:00"
# edit_time = "2021:11:19 21:30:00" # 迪士尼
# edit_time = "2020:12:16 19:55:00" # 哈尔滨


# 将 dir_path 目录里的所有照片都修改为 edit_time 时间（秒数会自增，保证时间不重复），并且
# 移动到 edit_time_path 里对应的月份文件夹
# 不支持 HEIC，PNG
if __name__ == '__main__':
    if os.path.isdir(dir_path):
        scan_dir(dir_path)
    else:
        try:
            my_utils.change_file_time(dir_path, edit_time)
            # my_utils.move_to_month_dir(dir_path, edit_time_path)
        except Exception as e:
            print(e)
