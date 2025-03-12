import yaml
import os
from utils.csv2md import csv_to_markdown
import json


# def read_md_files_from_directory(directory):
#     """
#     读取指定目录下所有`.md`文件的内容，并将它们作为一个长字符串返回。
#     如果目录不存在或目录中没有.md文件，将返回相应的提示信息。
#     """
#     md_content = ""
#     if not os.path.isdir(directory):
#         return "指定的路径不存在或不是一个目录。"
#     log_csv_path = os.path.join(directory, 'log.csv')
#     trace_csv_path = os.path.join(directory, 'trace.csv')
#     metric_csv_path = os.path.join(directory, 'metric.csv')

#     md_content += csv_to_markdown(log_csv_path)
#     md_content += '\n'
#     md_content += csv_to_markdown(trace_csv_path)
#     md_content += '\n'
#     md_content += csv_to_markdown(metric_csv_path)
    
#     return md_content.strip()   # 移除末尾多余的空行

def read_md_files_in_data_kind(directory, data_kind):
    data_content = ""
    if not os.path.isdir(directory):
        return "指定的路径不存在或不是一个目录。"
    data_csv_path = os.path.join(directory, data_kind)
    data_content += csv_to_markdown(data_csv_path)    
    return data_content.strip()   # 移除末尾多余的空行

def read_md_files_from_directory(directory):
    """
    读取指定目录下所有`.md`文件的内容，并将它们作为一个长字符串返回。
    如果目录不存在或目录中没有.md文件，将返回相应的提示信息。
    """
    md_content = ""
    if not os.path.isdir(directory):
        return "指定的路径不存在或不是一个目录。"
    
    md_content += read_md_files_in_data_kind(directory, 'log.csv')
    md_content += '\n'
    md_content += read_md_files_in_data_kind(directory, 'trace.csv')
    md_content += '\n'
    md_content += read_md_files_in_data_kind(directory, 'metric.csv')
    return md_content.strip()   # 移除末尾多余的空行

def read_yaml_file(file_path):
    """读取yaml文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用safe_load方法加载yaml文件内容
        data = yaml.safe_load(file)
    return data



def alldata():
    return read_md_files_from_directory(get_fault_path())

def partdata(kind):
    return read_md_files_in_data_kind(get_fault_path(), kind)

def get_fault_path():
    # 指定yaml文件路径
    yaml_file_path = 'config.yaml'
    # 调用函数读取并打印yaml文件内容
    config_data = read_yaml_file(yaml_file_path)
    root_path = 'TrainTicket'
    root_path = os.path.join(root_path, config_data['fault'])
    return root_path

def read_txt_as_json():
    file_path = os.path.join(get_fault_path(), 'fault.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        data = json.loads(content)
    return data
