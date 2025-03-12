import pandas as pd
import os
from datetime import datetime, timedelta

# 处理步骤1 将日志按照故障索引提取

# 读取groundtruth.csv（假设列包含st_time, ed_time和其他字段）
groundtruth = pd.read_csv("/home/leo/new_gaia/2021-07-04/groundtruth.csv")

# 读取log.csv并转换Unix时间戳
log = pd.read_csv("/home/leo/new_gaia/2021-07-04/log/log.csv")

# 将Unix时间戳转换为北京时间（UTC+8）
log["beijing_time"] = pd.to_datetime(log["timestamp"], unit="s") + timedelta(hours=8)

# # 遍历groundtruth的每一行
for idx, row in groundtruth.iterrows():
    folder_name = f"after_gaiya/F_{idx + 1}"
    os.makedirs(folder_name, exist_ok=True)

    # 保存当前行内容为txt
    with open(f"{folder_name}/groundtruth.txt", "w", encoding="utf-8") as f:
        f.write(f"Ground Truth Record {idx + 1}\n")
        for col in groundtruth.columns:
            f.write(f"{col}: {row[col]}\n")

    # 解析带毫秒的时间字符串（格式：2021-07-04 00:37:11.553000）
    st_time = pd.to_datetime(row["st_time"], format="%Y-%m-%d %H:%M:%S.%f")
    ed_time = pd.to_datetime(row["ed_time"], format="%Y-%m-%d %H:%M:%S.%f")

    # 筛选log数据（注意：这里log.beijing_time是UTC+8的时区）
    filtered_log = log[
        (log["beijing_time"] >= st_time) &
        (log["beijing_time"] <= ed_time)
        ]

    # 保存结果（保留原始timestamp列和转换后的beijing_time）
    filtered_log.to_csv(f"{folder_name}/filtered_log.csv",
                        columns=["timestamp", "beijing_time"] + list(
                            log.columns.difference(["timestamp", "beijing_time"])),
                        index=False)

print("处理完成！")
