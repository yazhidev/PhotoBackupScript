# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import get_time
import my_utils


# 扫描 root_path 的图片，将时间重复的图片复制到 repeat_time_file_path 目录下，以时间存储。不重复的图片不做处理

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            process_file(file_name)

def process_file(path):
    if my_utils.isPic(path):
        time = get_time.get_file_time(path)
        # print(time)
        if len(time) != 0:
            print("无时间图片：", path)
        else:
            if time in time_map:
                # 重复
                print("重复")
                month = time.replace(":", "-")
                month = month.replace(" ", "-")
                month_dir = repeat_time_file_path + month + "/"
                my_utils.move_file(path, month_dir)
                repeat_time_set.add(time)
            else:
                # print("pass")
                time_map[time] = path
    elif my_utils.isVideo(path):
        time = get_time.get_file_time(path)
        if len(time) == 0:
            print("无时间视频：", path)
        else:
            print("时间：", time)
            # month_time = time[0:6]
            # month = month_time[0:4] + "-" + month_time[4:6]
            # month_dir = normal_video_path + month + "/"
            # move_file(path, month_dir)
    else:
        print("无用文件")
        my_utils.move_file(path, delete_path)



unnormal_image_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_image/"
unnormal_png_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_png/"
unnormal_video_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_video/"
normal_image_path = "/Users/yazhi/Documents/11_edit_backup/normal_image/"
normal_video_path = "/Users/yazhi/Documents/11_edit_backup/normal_video/"
delete_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

time_map = {}
repeat_time_set = set()

# root_path = "/Users/yazhi/Documents/11_edit_backup/normal_image"
# root_path = "/Users/yazhi/Documents/11_edit_backup/test/testpath/2017-06"
# root_path = "/Users/yazhi/Downloads/photo/佳能相机/"
root_path = "/Users/yazhi/Documents/11_edit_backup/origin"
repeat_time_file_path = "/Users/yazhi/Documents/11_edit_backup/repeat_time_file/"

# 遍历 root_path，找出时间重复的图片(不处理视频)复制到 repeat_time_file_path（需要以/结尾）
if __name__ == '__main__':
    # 遍历文件夹，读取文件名
    # path = "/Users/yazhi/Documents/11_edit_backup/normal_image/2019-11"
    # path = "/Users/yazhi/Documents/11_edit_backup/origin"
    scan_dir(root_path)
    # 将有重复的图片取出
    for value in repeat_time_set:
        path = time_map.get(value)
        month = value.replace(":", "-")
        month = month.replace(" ", "-")
        month_dir = repeat_time_file_path + month + "/"
        my_utils.move_file(path, month_dir)



