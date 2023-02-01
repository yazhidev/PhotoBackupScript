# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import re
import time
import exifread
from hachoir import metadata
from hachoir import parser
from pyexiv2 import Image

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
            print(file_name)
            time = get_file_time(file_name)
            print(time)

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
    # print(myList)

    res = ""
    for i in range(1,len(myList)+1):
        #如果字符串在列表中,则提取数字部分,即为文件创建时间
        if myChar in myList[i-1]:
            fileTime = re.sub(r"\D",'',myList[i-1])    #使用正则表达式将列表中的非数字元素剔除
            a=list(fileTime)                           #将文件创建时间字符串转为列表list
            a.insert(timePosition,'_')                 #将列表插入下划线分割date与time
            res = change_video_format("".join(a))
    return res

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

# root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/test/aa"
# root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/test/IMG_0797.HEIC"
# 2022:05:02 12:16:49
root_path = "/Users/yazhi/Documents/11_edit_backup/待修改时间/重复时间照片都要"
# 2017:12:24 08:39:14

# 打印出 root_path 下所有文件的时间
if __name__ == '__main__':
    if os.path.isdir(root_path):
        scan_dir(root_path)
    else:
        res = get_file_time(root_path)
        print(res)





