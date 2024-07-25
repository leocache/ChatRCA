import re
from Agents import *
from Tooluse import *
from CSV2md import remove_suffix


if __name__ == '__main__':
    fault_time = read_txt_as_json()["inject_time"]
    fault_pod_suffix = read_txt_as_json()["inject_pod"]
    fault_pod = remove_suffix(remove_suffix(fault_pod_suffix))
    prompt = alldata() + '\n' +"""You are an operations engineer who is proficient in root cause analysis of cloud events.Existing fault types include return, exception, network delay, cpu content.
    The current cloud system experienced a failure at """ + fault_time + """. The current """ + fault_pod  + """service is affected. Please analyze the root cause.You are responsible for predicting root cause base on existing data. Do not give results beyond the four failure types in the current system.
    """
    User_proxy.initiate_chat(
        Assistant,
        message=prompt,
    )