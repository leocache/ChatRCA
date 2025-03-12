from utils.csv2md import *
from utils.read_file import *
from utils.skills4tt import *

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


