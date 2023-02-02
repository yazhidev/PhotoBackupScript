# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os

import get_time
import my_utils

a_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间"
b_path = "/Users/yazhi/Documents/11_edit_backup/无法修改/"

# 从 A 文件夹（！！记得使用副本）中移除无法被修改时间的图片到 B_path（要以/结尾）
if __name__ == '__main__':
    # 遍历文件夹，读取文件名
    for fpath, dirname, fnames in os.walk(a_path):
        for name in fnames:
            if "DS_Store" in name:
                continue
            file_name = fpath + "/" + name
            print(file_name)
            new_time = "2033:02:01 21:30:00"
            try:
                my_utils.change_file_time(file_name, new_time)
            except Exception as e:
                print(e)
            after_change_time_str = get_time.get_file_time(file_name)
            if after_change_time_str != new_time:
                print("时间与指定不同，文件无法被修改时间", file_name)
                my_utils.move_file(file_name, b_path)
            else:
                print("修改成功")

