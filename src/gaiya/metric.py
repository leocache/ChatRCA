import os
import pandas as pd
from datetime import timedelta

from tqdm import tqdm

# Load the groundtruth data
groundtruth = pd.read_csv('/home/leo/new_gaia/2021-07-04/groundtruth.csv')

# Create directories for each time period

# Process each row in the groundtruth file
for index, row in tqdm(groundtruth.iterrows(), total=groundtruth.shape[0], desc="Processing rows"):
    st_time = pd.to_datetime(row['st_time'], format="%Y-%m-%d %H:%M:%S.%f")
    ed_time = pd.to_datetime(row['ed_time'], format="%Y-%m-%d %H:%M:%S.%f")
    folder_name = f'after_gaiya/F_{index + 1}/metric'
    os.makedirs(folder_name, exist_ok=True)
    # Process each metric file
    metric_files = [f for f in os.listdir('/home/leo/new_gaia/2021-07-04/metric') if f.endswith('.csv')]
    for metric_file in tqdm(metric_files, desc="Processing metric files", leave=False):
        metric_data = pd.read_csv(os.path.join('/home/leo/new_gaia/2021-07-04/metric', metric_file))
        # Convert timestamp to Beijing time
        metric_data['beijing_time'] = pd.to_datetime(metric_data['timestamp'], unit='s') + timedelta(hours=8)
        # Filter the data for the given time period
        filtered_data = metric_data[(metric_data['beijing_time'] >= st_time) & (metric_data['beijing_time'] <= ed_time)]
        # Save the filtered data to the corresponding folder
        filtered_data.to_csv(os.path.join(folder_name, metric_file), index=False)
