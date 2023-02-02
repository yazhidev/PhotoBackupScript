# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os

import my_utils

a_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间"
b_path = "/Users/yazhi/Documents/11_edit_backup/无法修改"
c_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

# 从 A 文件夹中移除 B 文件夹中存在的文件到 C 中
if __name__ == '__main__':
    # 遍历文件夹，读取文件名
    have_files = set()
    for fpath, dirname, fnames in os.walk(b_path):
        for name in fnames:
            print(name)
            have_files.add(name)
    for fpath, dirname, fnames in os.walk(a_path):
        for name in fnames:
            if name in have_files:
                file_name = fpath + "/" + name
                my_utils.move_file(file_name, c_path)

