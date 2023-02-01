# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import re
import shutil
from pyexiv2 import Image
import exifread
from hachoir import metadata
from hachoir import parser


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
        # print("move %s -> %s" % (srcfile, dstpath + fname))

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

def isPng(path):
    if path.endswith(".png") \
            or path.endswith(".PNG"):
        return True
    else:
        return False

def isVideo(path):
    if path.endswith(".MOV") \
            or path.endswith(".mp4") \
            or path.endswith(".MP4") \
            or path.endswith(".mov"):
        return True
    else:
        return False

def process_file(path):
    if isPic(path):
        time = get_image_time(path)
        print(time)
        if len(time) == 0:
            print("无时间图片：", path)
            if isPng(path):
                move_file(path, unnormal_png_path)
            else:
                move_file(path, unnormal_image_path)
        else:
            if time in time_map:
                # 重复
                print("重复")
                month = time.replace(":", "-")
                month = month.replace(" ", "-")
                month_dir = repeat_time_file_path + month + "/"
                move_file(path, month_dir)
                repeat_time_set.add(time)
            else:
                # print("pass")
                time_map[time] = path
    elif isVideo(path):
        time = get_image_time(path)
        if len(time) == 0:
            print("无时间视频：", path)
            move_file(path, unnormal_video_path)
        else:
            print("时间：", time)
            # month_time = time[0:6]
            # month = month_time[0:4] + "-" + month_time[4:6]
            # month_dir = normal_video_path + month + "/"
            # move_file(path, month_dir)
    else:
        print("无用文件")
        move_file(path, delete_path)

def get_video_time(file,filetype="",myChar='Creation date',timePosition=8):
    """解析音频或者照片文件,
    :param file: 解析文件
    :param filetype: 待解析文件的类型
    :param myChar: 解析字符
    :param timePosition: 解析出来的字符添加下划线的位置,如:20161212161616,变成20161212_161616
    :return fileFinalTime: 解析出的文件创始时间
    """
    parserFile = parser.createParser(file) #解析文件
    if not parserFile:
        print("Unable to parse file - {}\n".format(file))
        return False
    try:
        metadataDecode = metadata.extractMetadata(parserFile)  # 获取文件的metadata
    except ValueError:
        print('Metadata extraction error.')
        metadataDecode = None
        return False

    if not metadataDecode:
        print("Unable to extract metadata.")
        return False


    myList = metadataDecode.exportPlaintext(line_prefix="") # 将文件的metadata转换为list,且将前缀设置为空
    # print(myList)

    time = ""
    for i in range(1,len(myList)+1):
        #如果字符串在列表中,则提取数字部分,即为文件创建时间
        if myChar in myList[i-1]:
            fileTime = re.sub(r"\D",'',myList[i-1])    #使用正则表达式将列表中的非数字元素剔除
            a=list(fileTime)                           #将文件创建时间字符串转为列表list
            a.insert(timePosition,'_')                 #将列表插入下划线分割date与time
            fileFinalTime = "".join(a)                 #重新将列表转为字符串
            time = fileFinalTime
    return time


def get_image_time(path):
    time = ""
    # print(path)
    if isPic(path):
        f = open(path, 'rb')
        tags = exifread.process_file(f)
        # 2020:10:11 09:42:31
        time = str(tags.get('EXIF DateTimeOriginal', ""))
        if len(time) == 0:
            # print("exifread 读取不到时间，尝试使用 pyexiv2")
            try:
                test = Image(path)
                data = test.read_exif()
                time = data.get('Exif.Photo.DateTimeOriginal', "")
                if len(time) != 0:
                    print("pyexiv2 读取时间成功", path)
            except Exception as e:
                print(e)
    elif isVideo(path):
        f = open(path, 'rb')
        time = get_video_time(f)
    return time

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

# root_path 里的子文件夹里的存在重复名字、且拍摄时间重复的照片
# 该脚本会将时间重复、名字重复（包括后缀（1）这种）的照片，只取大小最小的那张
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
                        move_file(value, need_image_path)
                    else:
                        move_file(value, delete_image_path)






