from agents import *
from utils import get_fault_info, get_fault_type_census
import re

def remove_suffix(text):
    # 清除倒数第一个“-”及以后的字符
    pattern = r'-[^-]*$'
    result = re.sub(pattern, '', text)
    return result

def run_TrainTicket_fault(): 
    tt_info = get_fault_info("TrainTicket", 'fault.txt', 'json')
    tt_desc = tt_info["fault_description"]
    fault_time = tt_desc["inject_time"]
    fault_pod_suffix =tt_desc["inject_pod"]
    fault_pod = remove_suffix(remove_suffix(fault_pod_suffix))
    chat_result = User_proxy.initiate_chat(
        Group_chat_manager,
        message="The current cloud system experienced a failure at " + fault_time + ". The current " + fault_pod + " service is affected. Please analyze the root cause.",
    )

def run_GAIA_fault(): 
    gy_info = get_fault_info("GAIA", 'groundtruth.txt', 'txt')
    gy_desc = gy_info["fault_description"]
    fault_date = gy_desc["date"]
    fault_service = gy_desc["service"]
    fault_message = gy_desc["message"]
    fault_start_time = gy_desc["st_time"]
    fault_ed_time = gy_desc["ed_time"]
    chat_result = User_proxy.initiate_chat(
        Group_chat_manager,
        message=f"The current cloud system experienced a failure from {fault_start_time} to {fault_ed_time}. The current {fault_service} service is affected. Please analyze the root cause.",
    )

if __name__ == '__main__':
    # run_TrainTicket_fault()
    run_GAIA_fault()
    # get_fault_type_census("GAIA", 'groundtruth.txt', 'txt', "anomaly_type")