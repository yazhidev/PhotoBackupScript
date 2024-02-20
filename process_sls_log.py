import os
import sys

# 处理 sls 日志，将 logstr 前的日志都清楚

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("参数错误")
    else:
        sls_log_file = sys.argv[1]
        file_name = os.path.basename(sls_log_file)
        index = find_last(file_name, '.')
        output_file_name = file_name[0:index] + "_processed" + file_name[index: len(file_name)]
        output_file_path = os.path.dirname(sls_log_file) + "/" + output_file_name
        # 打开源文件和目标文件
        with open(sls_log_file, 'r') as source_file, open(output_file_path, 'w') as output_file:
            # 逐行读取源文件
            for line in source_file:
                # 处理每一行
                index = find_last(line, 'logstr=')
                # 将处理后的行写入目标文件
                output_file.write(line[index: len(line)-1] + "---")
                output_file.write(line[0: index])
                output_file.write("\n")
        print("输出文件：" + output_file_path)