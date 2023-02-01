import pyexiv2
# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
from pyexiv2 import Image
import os
import re
import shutil
import exifread
from hachoir import metadata
from hachoir import parser

unnormal_image_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_image/"
unnormal_video_path = "/Users/yazhi/Documents/11_edit_backup/unnormal_video/"
normal_image_path = "/Users/yazhi/Documents/test/未命名文件夹/"
normal_video_path = "/Users/yazhi/Documents/11_edit_backup/normal_video/"
delete_path = "/Users/yazhi/Documents/11_edit_backup/delete/"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


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
        if len(time) == 0:
            move_file(path, unnormal_image_path)
        else:
            print("时间：", time)
            month_time = time[0:7]
            month = month_time.replace(":", "-")
            month_dir = normal_image_path + month + "/"
            move_file(path, month_dir)
    elif isVideo(path):
        time = get_image_time(path)
        if len(time) == 0:
            move_file(path, unnormal_video_path)
        else:
            print("时间：", time)
            month_time = time[0:6]
            month = month_time[0:4] + "-" + month_time[4:6]
            month_dir = normal_video_path + month + "/"
            move_file(path, month_dir)
    else:
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


def get_image_time(path):
    time = ""
    print(path)
    if isPic(path):
        f = open(path, 'rb')
        tags = exifread.process_file(f)
        # 2020:10:11 09:42:31
        time = str(tags.get('EXIF DateTimeOriginal', ""))
    elif isVideo(path):
        f = open(path, 'rb')
        time = get_video_time(f)
    return time

if __name__ == '__main__':
    print_hi('PyCharm')
    path = "/Users/yazhi/Documents/11_edit_backup/origin/Takeout 5/Google Photos/Photos from 2020/IMG_3917.JPG"
    # test = Image(path)
    # data = test.read_exif()
    # print('拍摄时间：', data.get('Exif.Photo.DateTimeOriginal', ""))

    # test.modify_exif({'Exif.Photo.DateTimeOriginal': '2020:01:27 08:13:28'})
    # print(test.read_exif())

    # f = open(path, 'rb')
    # tags = exifread.process_file(f)
    # time = tags.get('EXIF DateTimeOriginal', "")
    # print('拍摄时间：', time)


    # test = Image('/Users/yazhi/Documents/test/1526133570225_reborn.JPG')
    # print(test.read_exif())
    # test2 = Image('/Users/yazhi/Documents/test/IMG_20180127_081328.jpg')
    # print(test2.read_exif())

    # 遍历文件夹，读取文件名
    path = "/Users/yazhi/Documents/11_edit_backup/origin"
    scan_dir(path)

