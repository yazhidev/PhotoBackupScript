# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os

import get_time
import my_utils

unnormal_image_path = "/Users/yazhi/Documents/11_edit_backup/xx/unnormal_image/"
# unnormal_image_path = "/Users/yazhi/Documents/11_edit_backup/xx/normal_image"
unnormal_png_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_png/"
unnormal_video_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_video/"
# normal_image_path = "/Users/yazhi/Documents/11_edit_backup/normal_image/"
normal_image_path = "/Users/yazhi/Documents/11_edit_backup/xx"
normal_video_path = "/Users/yazhi/Documents/11_edit_backup/normal_video/"
delete_path = "/Users/yazhi/Documents/11_edit_backup/delete/"
move_no_time_file = False
def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            process_file(file_name)

def process_file(path):
    print(path)
    if my_utils.isPic(path):
        time = get_time.get_file_time(path)
        if len(time) == 0:
            print("无时间图片：", path)
            if move_no_time_file:
                if my_utils.isPng(path):
                    my_utils.move_file(path, unnormal_png_path)
                else:
                    my_utils.move_file(path, unnormal_image_path)
        else:
            # print("时间：", time)
            month_time = time[0:7]
            month = month_time.replace(":", "-")
            month_dir = normal_image_path + month + "/"
            my_utils.move_file(path, month_dir)
    elif my_utils.isVideo(path):
        time = get_time.get_file_time(path)
        if len(time) == 0:
            print("无时间视频：", path)
            if move_no_time_file:
                my_utils.move_file(path, unnormal_video_path)
        else:
            # print("时间：", time)
            month_time = time[0:6]
            month = month_time[0:4] + "-" + month_time[4:6]
            month_dir = normal_video_path + month + "/"
            my_utils.move_file(path, month_dir)
    else:
        my_utils.move_file(path, delete_path)

# root_path = "/Users/yazhi/Documents/11_edit_backup/origin"
root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间副本"


if __name__ == '__main__':
    # 遍历文件夹，读取文件名
    scan_dir(root_path)

