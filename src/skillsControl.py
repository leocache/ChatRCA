from tooluse import *

def alldata() -> str:
    return read_md_files_from_directory(get_fault_path())

def partdata(kind):
    return read_md_files_in_data_kind(get_fault_path(), kind)

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
    kind = 'log.csv'
    directory = get_fault_path()
    logs_data = read_md_files_in_data_kind(directory, kind)
    error_logs = filter_error_logs(logs_data)
    return error_logs


def process_metric_data():
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'metric.csv'
    directory = get_fault_path()
    metric_data = read_md_files_in_data_kind(directory, kind)
    filtered_metrics = filter_metric_data(metric_data)
    return filtered_metrics

def process_trace_data():
    # 提供给agent的处理日志文件功能
    # 提取异常数据并返回为md格式
    kind = 'trace.csv'
    directory = get_fault_path()
    trace_data = read_md_files_in_data_kind(directory, kind)
    filtered_traces = filter_trace_data(trace_data)
    return filtered_traces