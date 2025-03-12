import pandas as pd
import os
#处理步骤6 删除日志和链路中没有ERROR的trace_id记录
# 定义删除函数
def delete_non_error_logs(base_folder):
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            log_file_path = os.path.join(folder_path, "filtered_log.csv")
            trace_file_path = os.path.join(folder_path, "filtered_trace.csv")

            if os.path.exists(log_file_path) and os.path.exists(trace_file_path):
                # 读取filtered_log.csv
                log_df = pd.read_csv(log_file_path)
                # 读取filtered_trace.csv
                trace_df = pd.read_csv(trace_file_path)
                # 找出所有trace_id
                trace_ids = log_df['trace_id'].unique()
                # 遍历每一个trace_id
                for trace_id in trace_ids:
                    # 获取该trace_id的所有日志
                    trace_logs = log_df[log_df['trace_id'] == trace_id]
                    # 检查是否所有log_level都不是ERROR
                    if not (trace_logs['log_level'] == 'ERROR').any():
                        # 删除log_df中该trace_id的所有日志
                        log_df = log_df[log_df['trace_id'] != trace_id]
                        # 删除trace_df中该trace_id的所有记录
                        trace_df = trace_df[trace_df['trace_id'] != trace_id]

                # 保存结果
                log_df.to_csv(log_file_path, index=False)
                trace_df.to_csv(trace_file_path, index=False)

# 设置基础文件夹路径
base_folder = "/home/leo/code/ChatRCA/src/gaiya/after_gaiya"
delete_non_error_logs(base_folder)

print("处理完成！")