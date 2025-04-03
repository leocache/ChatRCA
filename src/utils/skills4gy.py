from utils.read_file import *
from utils.filter_tools import *

dataset = 'GAIA'
def alldata() -> str:
    return read_md_files_from_directory(get_fault_path(dataset))

def partdata(name) -> str:
    return read_md_files_in_name(get_fault_path(dataset), name)

def architectureData() ->str:
    # 读取架构信息 
    filepath = get_architecture_path()
    filename = dataset + '.md'
    path = os.path.join(filepath, filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"The {filename} file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def process_log_data() -> str:
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'filtered_log.csv'
    directory = get_fault_path(dataset)
    logs_data = read_md_files_in_name(directory, kind)
    error_logs = filter_error_logs(logs_data)
    return error_logs

def process_metric_data() -> dict[str, str]:
    kind = 'metric' # metric文件夹名称，GAIA数据集的metric在metric文件夹下
    directory = get_fault_path(dataset)
    directory = os.path.join(directory, kind)
    metric_data = {}
    for filename in os.listdir(directory):
        content = read_md_files_in_name(directory, filename)
        if content is "":
            continue
        metric_data[filename] = content
    # filtered_metric = filter_metric_data(metric_data)
    return metric_data

def process_trace_data() -> str:
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'filtered_trace.csv'
    directory = get_fault_path(dataset)
    trace_data = read_md_files_in_name(directory, kind)
    filtered_traces = filter_trace_data(trace_data)
    return filtered_traces