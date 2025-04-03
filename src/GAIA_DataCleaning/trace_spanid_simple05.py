import pandas as pd
import os

#处理步骤5 简化span_id
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

        if os.path.exists(trace_file_path):
            # 读取filtered_trace.csv
            trace_df = pd.read_csv(trace_file_path)
            # 简化span_id
            span_id_map = simplify_ids(trace_df, "span_id", "s")
            # 简化parent_id，确保与span_id一致
            trace_df["parent_id"] = trace_df["parent_id"].map(span_id_map)
            # 保存结果
            trace_df.to_csv(trace_file_path, index=False)

print("处理完成！")