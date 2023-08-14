# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import re
import time
import exifread
from hachoir import metadata
from hachoir import parser
from pyexiv2 import Image

import get_time

unnormal_path = "/Users/yazhi/Documents/11_edit_backup/unnormal/"
normal_path = "/Users/yazhi/Documents/11_edit_backup/normal/"
video_path = "/Users/yazhi/Documents/11_edit_backup/video/"
delete_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            if ".DS_Store" in file_name:
                continue
            process_file(file_name)

# 20171224_083914 转 2017:12:24 08:39:14
def change_video_format(str):
    # 20171224_083914
    # 先转换为时间数组
    time_array = time.strptime(str, "%Y%m%d_%H%M%S")
    # 转换为时间戳
    time_stamp = int(time.mktime(time_array))
    # 转回时间字符串
    time_array = time.localtime(time_stamp)
    return time.strftime("%Y:%m:%d %H:%M:%S", time_array)

def process_file(path):
    index = path.rfind("/")
    str = get_time.get_file_time(path)
    if len(str) != 0:
        time_str = str.replace(":", "").replace(" ", "-")
        # 找到原名
        if path[index + 9] == "-" and path[index + 16] == "-":
            # 名字里已经带了时间了
            time_of_name = path[index + 1:index + 16]
            if time_of_name != time_str:
                old_name = path[index + 17:]
                new_name = path[0:index + 1] + time_str + "-" + old_name
                print("旧名字里的时间", time_of_name)
                print("时间不对，重命名", new_name)
                os.renames(path, new_name)
            else:
                print("已命名过")
        else:
            index = path.rfind("/")
            new_name = path[0:index + 1] + time_str + "-" + path[index + 1:]
            print("重命名", new_name)
            os.renames(path, new_name)
    else:
        print("获取时间失败，跳过", path)

# root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/test/aa"
# root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/test/IMG_0797.HEIC"
# 2022:05:02 12:16:49
root_path = "/Users/yazhi/Documents/11_edit_backup/normal_image"
# 2017:12:24 08:39:14

# root_path 下所有文件重命名为 年月日-时分秒-原名
if __name__ == '__main__':
    scan_dir(root_path)
    # process_file(root_path)






