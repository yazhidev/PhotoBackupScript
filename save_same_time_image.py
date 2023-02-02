import os
import time

import exifread
from hachoir import metadata
from hachoir import parser
from pyexiv2 import Image

import get_time
import my_utils

# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md


# PNG 图片使用 modify_exif 修改无效（exifread 无法读取到，上传到一刻时间也不对）

root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/重复时间照片都要"

# dir_path 下的所有目录里的照片时间是重复的，但是这些照片又确实需要共存
# 需要结构为：
# root_path
#   --2029-12
#       --a.jpg
#       --b.jpg
# 使用该脚本会将重复时间的照片秒数自增，保证时间不重复
if __name__ == '__main__':
    dirs = os.listdir(root_path)
    for dir in dirs:
        this_dir_time = ""
        dir_path = root_path + "/" + dir
        if ".DS_Store" in dir_path:
            continue
        files = os.listdir(dir_path)
        for file in files:
            file_name = dir_path + "/" + file
            if ".DS_Store" in file_name:
                continue
            print(file_name)
            if len(this_dir_time) == 0:
                # 读取本文件夹照片时间
                this_dir_time = get_time.get_file_time(file_name)
                print(this_dir_time)
            else:
                #秒数自增
                this_dir_time = my_utils.update_edit_time(this_dir_time)
                try:
                    my_utils.change_file_time(file_name, this_dir_time)
                except Exception as e:
                    print(e)


