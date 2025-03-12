import pandas as pd
import os

# 处理步骤4 简化trace_id（包括日志和链路中的）
# 定义简化函数
def simplify_ids(df, column_name, prefix):
    unique_ids = df[column_name].unique()
    id_map = {uid: f"{prefix}{i + 1}" for i, uid in enumerate(unique_ids)}
    df[column_name] = df[column_name].map(id_map)
    return id_map

# 遍历after_gaiya文件夹中的每一个F_i文件夹
base_folder = "/home/leo/code/ChatRCA/src/gaiya/after_gaiya"
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    if os.path.isdir(folder_path):
        trace_file_path = os.path.join(folder_path, "filtered_trace.csv")
        log_file_path = os.path.join(folder_path, "filtered_log.csv")

        if os.path.exists(trace_file_path):
            # 读取filtered_trace.csv
            trace_df = pd.read_csv(trace_file_path)
            # 简化trace_id
            trace_id_map = simplify_ids(trace_df, "trace_id", "t")
            # 保存结果
            trace_df.to_csv(trace_file_path, index=False)

        if os.path.exists(log_file_path):
            # 读取filtered_log.csv
            log_df = pd.read_csv(log_file_path)
            # 更新log_df中的trace_id
            log_df["trace_id"] = log_df["trace_id"].map(trace_id_map)
            # 删除trace_id不存在于trace_id_map中的记录
            log_df = log_df[log_df["trace_id"].notna()]
            # 保存结果
            log_df.to_csv(log_file_path, index=False)

print("处理完成！")