import yaml
import os
import json
import glob
from utils.csv2md import csv_to_markdown

def read_md_files_in_name(directory, filename):
    """
    读取指定目录下的Markdown文件内容，并将CSV内容转换为Markdown格式。

    @param:
    directory (str): 指定的目录路径。
    filename (str): 用于指定特定的文件名。包括log、trace和metric, 不包含扩展名。

    @return:
    str: 转换后的Markdown内容或错误信息。
    """
    data_content = ""

    if not os.path.isdir(directory):
        return "指定的路径不存在或不是一个目录。"
    
    data_csv_path = os.path.join(directory, filename)
    data_content += csv_to_markdown(data_csv_path)
    return data_content.strip()   # 移除末尾多余的空行

# def read_md_files_from_directory(directory):
#     """
#     读取指定目录下所有`.md`文件的内容，并将它们作为一个长字符串返回。
#     如果目录不存在或目录中没有.md文件，将返回相应的提示信息。
    
#     @param:
#     directory (str): 要读取的目录路径。
    
#     @return:
#     str: 所有.md文件的内容合并为一个长字符串，或者错误提示信息。
#     """
#     md_content = ""

#     if not os.path.isdir(directory):
#         return "指定的路径不存在或不是一个目录。"
    
#     md_content += read_md_files_in_name(directory, 'log.csv')
#     md_content += '\n'
#     md_content += read_md_files_in_name(directory, 'trace.csv')
#     md_content += '\n'
#     md_content += read_md_files_in_name(directory, 'metric.csv')
#     return md_content.strip()   # 移除末尾多余的空行

def read_md_files_from_directory(directory, kind = 'csv'):
    """
    读取指定目录下所有`.kind`文件的内容，并将它们作为一个长字符串返回。
    如果目录不存在或目录中没有.md文件，将返回相应的提示信息。
    
    @param:
    directory (str): 要读取的目录路径。
    kind (str): 文件种类，比如csv

    @return:
    str: 所有.md文件的内容合并为一个长字符串，或者错误提示信息。
    """
    md_content = ""

    if not os.path.isdir(directory):
        return "指定的路径不存在或不是一个目录。"
    
    # 使用glob.glob获取目录下所有.kind文件
    files = glob.glob(os.path.join(directory, f'*.{kind}'))
    
    if not files:
        return f"目录中没有{ kind }文件。"
    
    for file in files:
        md_content += read_md_files_in_name(directory, file)
        md_content += '\n'  # 添加换行符以分隔不同文件的内容
    
    return md_content.strip()   # 移除末尾多余的空行

def read_yaml_file(file_path):
    """读取yaml文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用safe_load方法加载yaml文件内容
        data = yaml.safe_load(file)
    return data

def get_fault_path(dir_name = 'TrainTicket'):
    """
    获取yaml文件中fault路径
    这个函数的目的是从yaml配置文件中读取并故障数据所在路径
    
    @ param:
    dir_name (str): 默认值为'TrainTicket'，表示数据目录的名称
    
    @return:
    str: 构造的故障路径
    """
    # 获取当前脚本所在的目录路径: src/utils/
    current_dir = os.path.dirname(__file__)
    # 指定yaml文件路径: /src/config.yaml
    yaml_file_path = os.path.join(current_dir, '..', 'config.yaml')
    # 调用函数读取并打印yaml文件内容
    config_data = read_yaml_file(yaml_file_path)

    # 获取根目录路径: /src/TrainTicket/
    root_path = os.path.join(os.path.dirname(current_dir), dir_name)
    # 获取故障路径: /src/TrainTicket/fault_x/
    root_path = os.path.join(root_path, config_data['fault'])
    # print(f"root_path: {root_path}")
    return root_path

def read_fault_description(directory, filename, kind):
    """
    读取 filename 文件 
    将指定的文本文件按kind格式解析并返回

    json用于D1:TranTicket数据集
    yaml用于D2:gaiya数据集

    参数:
    directory (str): 文件所在的目录
    filename (str): 文件名
    kind (str): 描述性文件的种类或类型, 比如json/yaml/txt

    返回:
    dict: 解析后的数据
    """
    file_path = os.path.join(directory, filename)
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        if kind == 'json':
            content = file.read()
            data = dict(json.loads(content))
        elif kind == 'yaml':
            data = dict(yaml.safe_load(content))
        elif kind == 'txt':
            lines = file.readlines()
            for line in lines:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    data[key.strip()] = value.strip()
    return data

