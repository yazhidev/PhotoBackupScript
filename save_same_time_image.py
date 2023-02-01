import os
import time

import exifread
from hachoir import metadata
from hachoir import parser
from pyexiv2 import Image


# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md


# PNG 图片使用 modify_exif 修改无效（exifread 无法读取到，上传到一刻时间也不对）

def scan_dir(path):
    full_path = path.replace("~", os.path.expanduser('~'))
    for fpath, dirname, fnames in os.walk(full_path):
        for name in fnames:
            file_name = fpath + "/" + name
            process_file(file_name)

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

def update_edit_time(now_time):
    # 先转换为时间数组
    time_array = time.strptime(now_time, "%Y:%m:%d %H:%M:%S")
    # 转换为时间戳
    time_stamp = int(time.mktime(time_array))
    # 自增
    time_stamp = time_stamp + 1
    # 转回时间字符串
    time_array = time.localtime(time_stamp)
    return time.strftime("%Y:%m:%d %H:%M:%S", time_array)

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

def get_file_time(path):
    if isPic(path):
        return get_image_time(path)
    elif isVideo(path):
        return get_video_time(path)
    else:
        print("非图片、视频")

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
    print(myList)

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

def get_file_time(path):
    if isPic(path):
        return get_image_time(path)
    elif isVideo(path):
        return get_video_time(path)
    else:
        print("非图片、视频")

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
                this_dir_time = get_file_time(file_name)
                print(this_dir_time)

            else:
                #秒数自增
                this_dir_time = update_edit_time(this_dir_time)
                try:
                    test = Image(file_name)
                    print("modify_time", this_dir_time)
                    test.modify_exif({'Exif.Photo.DateTimeOriginal': this_dir_time})
                except Exception as e:
                    print(e)


