from utils.csv2md import *
from utils.read_file import *
from utils.skills4tt import *
import os

def get_fault_info(dataset, des_filename, des_kind):
    # 获取fault_x数据所在目录
    fault_path = get_fault_path(dataset)
    # 获取fault.txt中的信息
    fault_description = read_fault_description(fault_path, des_filename, des_kind)

    md_files = read_md_files_from_directory(fault_path, 'csv')
    return {
        'fault_description': fault_description,
        'md_files': md_files
    }

def get_fault_type_census(dataset, des_filename, des_kind, type_des):
    # 获取数据集所在目录: 
    current_dir = os.path.dirname(__file__)
    father_dir = os.path.dirname(current_dir)
    faults_path = os.path.join(father_dir, dataset)
    print(faults_path)
    
    # 获取其下每个文件夹
    faults_dir = os.listdir(faults_path)
    i = 0
    for fault_dir in faults_dir:
        fault_dir = os.path.join(faults_path, fault_dir)
        # 获取fault.txt中的信息
        fault_description = read_fault_description(fault_dir, des_filename, des_kind)
        print(i, fault_description[type_des])
        i += 1
