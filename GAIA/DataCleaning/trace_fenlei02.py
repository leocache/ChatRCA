import pandas as pd
import os
from datetime import datetime, timedelta
# 处理步骤2 将链路按照故障索引提取
# 读取groundtruth.csv
groundtruth = pd.read_csv("/home/leo/new_gaia/2021-07-04/groundtruth.csv")

# 读取trace.csv并转换Unix时间戳
trace = pd.read_csv("/home/leo/new_gaia/2021-07-04/trace/trace.csv")
trace["beijing_time"] = pd.to_datetime(trace["timestamp"], unit="s") + timedelta(hours=8)
trace["beijing_end_time"] = pd.to_datetime(trace["ed_time"], unit="s") + timedelta(hours=8)
# 遍历groundtruth的每一行
for idx, row in groundtruth.iterrows():
    folder_name = f"after_gaiya/F_{idx + 1}"
    os.makedirs(folder_name, exist_ok=True)

    # 解析带毫秒的时间字符串（格式：2021-07-04 00:37:11.553000）
    st_time = pd.to_datetime(row["st_time"], format="%Y-%m-%d %H:%M:%S.%f")
    ed_time = pd.to_datetime(row["ed_time"], format="%Y-%m-%d %H:%M:%S.%f")

    # 筛选trace数据（注意：这里trace.beijing_time是UTC+8的时区）
    filtered_trace = trace[
        (trace["beijing_time"] >= st_time) &
        (trace["beijing_time"] <= ed_time)
    ]

    # 保存结果（只保留指定的列）
    filtered_trace.to_csv(f"{folder_name}/filtered_trace.csv",
                          columns=["beijing_time", "message", "parent_id", "service_name", "span_id", "status_code",
                                   "trace_id"],
                          index=False)

print("处理完成！")