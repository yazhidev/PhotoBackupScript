# on mac,brew install gettext
# https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
import os
import zipfile

root_path = "/Users/yazhi/Documents/test_ima2/2023-33"
def scan_dir(path):
    zipPath(root_path)

def zipdir(path, ziph):
    print("开始压缩 " + path)
    # ziph是ZipFile对象
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
def zipPath(directory):
    # 获取目录下所有文件夹的名称
    # subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
    # 压缩文件存储路径
    parent_dir = os.path.dirname(directory)
    print(dir)
    # 设置压缩文件的名称和路径
    zipfilename = os.path.basename(directory)
    zipfilepath = os.path.join(directory, zipfilename)
    # 创建ZipFile对象并压缩文件夹
    zipf = zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED)
    zipdir(directory, zipf)
    zipf.close()
    print("压缩完成！")

if __name__ == '__main__':
    # 遍历文件夹，读取文件名
    scan_dir(root_path)

