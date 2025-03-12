from utils.read_file import *
from utils.filter_tools import *

def alldata() -> str:
    return read_md_files_from_directory(get_fault_path('gaiya'))

def partdata(name):
    return read_md_files_in_name(get_fault_path(), name)

def architectureData() ->str:
    # 读取架构信息 
    filepath = 'architecture.md'
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The architect.md file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def process_log_data():
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'filtered_log.csv'
    directory = get_fault_path()
    logs_data = read_md_files_in_name(directory, kind)
    error_logs = filter_error_logs(logs_data)
    return error_logs

def process_metric_data():
    return None

def process_trace_data():
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'filtered_trace.csv'
    directory = get_fault_path()
    trace_data = read_md_files_in_name(directory, kind)
    filtered_traces = filter_trace_data(trace_data)
    return filtered_traces