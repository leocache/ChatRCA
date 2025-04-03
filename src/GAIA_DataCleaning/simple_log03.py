import pandas as pd
import os

# 处理步骤3 删除日志中无关内容
# Define the function to extract and split the message field
def extract_message_info(df):
    # Split the message field using '|'
    split_columns = df['message'].str.split('|', expand=True)
    # Assign the split columns to the respective fields
    df['timestamp'] = split_columns[0].str.strip()
    df['log_level'] = split_columns[1].str.strip()
    df['service_name'] = df['service']
    df['trace_id'] = split_columns[5].str.strip()
    df['message'] = split_columns[6].str.strip()
    # Keep only the required columns
    df = df[['timestamp', 'log_level', 'service_name', 'trace_id', 'message']]
    return df

# Traverse each F_i folder in the after_gaiya directory
base_folder = "/home/leo/code/ChatRCA/src/gaiya/after_gaiya"
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    if os.path.isdir(folder_path):
        file_path = os.path.join(folder_path, "filtered_log.csv")
        if os.path.exists(file_path):
            # Read the filtered_log.csv file
            df = pd.read_csv(file_path)
            # Extract and split the message field
            df = extract_message_info(df)
            # Save the result
            df.to_csv(file_path, index=False)

print("Processing complete!")