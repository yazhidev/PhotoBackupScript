# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os

import my_utils

repeat_time_file_path = "/Users/yazhi/Documents/11_edit_backup/repeat_time_file/"

unnormal_image_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_image/"
unnormal_png_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_png/"
unnormal_video_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_video/"
normal_image_path = "/Users/yazhi/Documents/11_edit_backup/normal_image/"
normal_video_path = "/Users/yazhi/Documents/11_edit_backup/normal_video/"
delete_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

time_map = {}
repeat_time_set = set()

# root_path = "/Users/yazhi/Documents/11_edit_backup/test"
root_path = "/Users/yazhi/Documents/11_edit_backup/repeat_time_file"
need_image_path = "/Users/yazhi/Documents/11_edit_backup/need_image/"
delete_image_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

# 处理root_path 里的子文件夹里的重复名字且时间重复的照片
# root_path 需要结构为：
# root_path
#   --2029-12
#       --a.jpg
#       --a.HEIC
# 时间重复、名字重复（包括后缀（1）这种）的照片，只保留大小最小的那张（移动到 need_image_path），删除
# 的移动到 delete_image_path

if __name__ == '__main__':
    dirs = os.listdir(root_path)
    for dir in dirs:
        dir_path = root_path + "/" + dir
        if dir == ".DS_Store":
            print("")
        else:
            print(dir_path)
            files = os.listdir(dir_path)
            # 2. 同时存在 .HEIC 和 .jpeg 和 .JPG，只保留 jpeg
            # 3. 同时存在两个 jpeg，真的是时间相同
            heic_path = ""
            jpeg_path = ""
            jpg_path = ""

            # 名字相同，保留最小的那个文件
            name_set = set()
            path_set = set()
            for file in files:
                print(file)
                if file.rfind(" (") >= 0:
                    name = file[0:file.rfind(" (")]
                    print(name)
                elif file.rfind("(") >= 0:
                    name = file[0:file.rfind("(")]
                    print(name)
                else:
                    index = file.rfind(".")
                    name = file[0:index]
                    print(name)
                name_set.add(name)
                file_path = dir_path + "/" + file
                path_set.add(file_path)
            print(len(name_set))

            if len(name_set) == 1:
                save_path = ""
                min_size = 1884781300
                for file in files:
                    file_path = dir_path + "/" + file
                    stats = os.stat(file_path)
                    if min_size > stats.st_size:
                        save_path = file_path
                        min_size = stats.st_size
                print(save_path)
                for value in path_set:
                    if value == save_path:
                        my_utils.move_file(value, need_image_path)
                    else:
                        my_utils.move_file(value, delete_image_path)







