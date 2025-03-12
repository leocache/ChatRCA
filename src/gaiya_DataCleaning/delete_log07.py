# 处理步骤7 删除日志中非ERROR项
import pandas as pd
import os

# 定义删除INFO日志的函数
def delete_info_logs(base_folder):
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            log_file_path = os.path.join(folder_path, "filtered_log.csv")

            if os.path.exists(log_file_path):
                # 读取filtered_log.csv
                log_df = pd.read_csv(log_file_path)
                # 删除log_level为INFO的行
                log_df = log_df[log_df['log_level'] != 'INFO']
                # 保存结果
                log_df.to_csv(log_file_path, index=False)

# 设置基础文件夹路径
base_folder = "/home/leo/code/ChatRCA/src/gaiya/after_gaiya"
delete_info_logs(base_folder)

print("处理完成！")