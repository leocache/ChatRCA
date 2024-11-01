from src.agents import *
from tooluse import *
from src.csv2md import remove_suffix



if __name__ == '__main__':
    fault_time = read_txt_as_json()["inject_time"]
    fault_pod_suffix = read_txt_as_json()["inject_pod"]
    fault_pod = remove_suffix(remove_suffix(fault_pod_suffix))
    chat_result = User_proxy.initiate_chat(
        Group_chat_manager,
        message="The current cloud system experienced a failure at " + fault_time + ". The current " + fault_pod + " service is affected. Please analyze the root cause.",
    )
