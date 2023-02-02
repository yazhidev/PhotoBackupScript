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
edit_time = ""


def move_file(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))

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

def process_file(path):
    if isPic(path):
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

# 命名格式为：mmexport1640440673122
def process_file3(path, offset, process):
    print(path)
    index = path.rfind("/")
    time_int = path[index + offset:index + offset + 10]
    str_time = change_time_format3(time_int)
    print(str_time)
    if process:
        try:
            my_utils.change_file_time(path, str_time)
            my_utils.move_to_month_dir(path, edit_time_path)
        except Exception as e:
            print(e)

# 输入 1640441573
def change_time_format3(time_int):
    print(time_int)
    # 1640441573
    time_array = time.localtime(int(time_int))
    return time.strftime("%Y:%m:%d %H:%M:%S", time_array)


# 命名格式为：IMG_20171001_185152
def process_file6(path, left, right, format_str, process):
    print(path)
    index = path.rfind("/")
    str_time = change_time_format2(path[index+left:index+ right + left], format_str)
    print(str_time)
    if process:
        try:
            my_utils.change_file_time(path, str_time)
            my_utils.move_to_month_dir(path, edit_time_path)
        except Exception as e:
            print(e)

def change_time_format2(str, format_str):
    # 20171224_083914
    print(str)
    # 先转换为时间数组
    time_array = time.strptime(str, format_str)
    # 转换为时间戳
    time_stamp = int(time.mktime(time_array))
    # 转回时间字符串
    time_array = time.localtime(time_stamp)
    return time.strftime("%Y:%m:%d %H:%M:%S", time_array)

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            if ".DS_Store" in file_name:
                continue
            #命名带时间戳
            # mmexport1640440673122
            # process_file3(file_name, 9)
            # 命名格式为：1520746762255.jpg
            # process_file4(file_name)
            # 命名格式为：beauty_1573917227957
            # process_file5(file_name)
            # 命名格式为：wx_camera_1631757820018
            process_file3(file_name, 11, True)

            # 命名带日期
            # 命名格式为：beauty_20200201170809
            # process_file2(file_name)
            # 命名格式为：IMG_20171001_185152
            # process_file6(file_name, "IMG_", 4, 15, "%Y%m%d_%H%M%S")
            # 命名格式为：faceu_20171231174309.JPG
            # process_file6(file_name, "faceu_", 6, 14, "%Y%m%d%H%M%S")
            # 命名格式为：MTXX_20190824124226
            # process_file6(file_name, 6, 13, "%Y%m%d%H%M%S")
            # 命名格式为：WuTa_2018-03-10_13-27-29
            # process_file6(file_name, 6, 19, "%Y-%m-%d_%H-%M-%S", True)
            # 命名格式为：Screenshot_2020-10-30-22-50-20-331_com.riotgame
            # process_file6(file_name, 12, 19, "%Y-%m-%d-%H-%M-%S", True)


dir_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/重复时间照片都要"
# 修改后复制到该目录下
edit_time_path = "/Users/yazhi/Documents/11_edit_backup/origin/"

# 将 dir_path 目录里的所有照片的时间修改为名字里的时间，例如 beauty_20200201170809，则时间修改为 20200201 170809
# 不支持 HEIC
if __name__ == '__main__':
    if os.path.isdir(dir_path):
        scan_dir(dir_path)
