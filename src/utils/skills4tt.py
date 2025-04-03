from utils.read_file import *
from utils.filter_tools import *

dataset = 'TrainTicket'
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
    kind = 'log.csv'
    directory = get_fault_path(dataset)
    logs_data = read_md_files_in_name(directory, kind)
    error_logs = filter_error_logs(logs_data)
    return error_logs


def process_metric_data() -> str:
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'metric.csv'
    directory = get_fault_path(dataset)
    metric_data = read_md_files_in_name(directory, kind)
    filtered_metrics = filter_metric_data(metric_data)
    return filtered_metrics

def process_trace_data() -> str:
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'trace.csv'
    directory = get_fault_path(dataset)
    trace_data = read_md_files_in_name(directory, kind)
    filtered_traces = filter_trace_data(trace_data)
    return filtered_traces