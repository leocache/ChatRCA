from autogen import AssistantAgent, UserProxyAgent
from autogen import ConversableAgent
from autogen import GroupChatManager
from autogen import GroupChat
from autogen import register_function
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

from Tooluse import alldata
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv
from autogen import ConversableAgent
import os
import tempfile
# from autogen.agentchat.contrib.capabilities import transform_messages
# from autogen.agentchat.contrib.capabilities.text_compressors import LLMLingua
# from autogen.agentchat.contrib.capabilities.transforms import TextMessageCompressor

load_dotenv()
#, "base_url": os.environ.get("OPENAI_API_BASE")
config_list = {"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY"), "timeout": 100, "cache_seed": None}]}

temp_dir = tempfile.TemporaryDirectory()

# 代码执行器
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# 代码执行代理 负责调用代码执行器来执行代理
Operator = ConversableAgent(
    name='Operator',
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},
    description='An operator is responsible for executing the code of agent skills and interacting with external data sources.Can only be called by Observable_engineer_agent!',
)

# 用户代理 发布任务，介入人机交互
User_proxy = UserProxyAgent(
    name='User_proxy_agent',
    code_execution_config=False
)
# 总运维工程师
Operation_Engineer_Agent = ConversableAgent(
    name='OperationEngineer',
    llm_config= config_list,
    human_input_mode="ALWAYS",
    system_message="""
                    # CONTEXT #
                    This system is a cloud service train ticket sales system. Existing fault types include 
                    return,exception,network delay, cpu content. Return failures and exceptions usually need to be 
                    identified through traces and logs.
                    
                    #############
                    
                    # ROLE #
                    You are an operations engineer who is proficient in root cause analysis of cloud events.
                
                    #############
                    
                    # OBJECTIVE #
                    Task: You are responsible for referring to the analysis of other experts and combining your own 
                    knowledge and experience to determine the root cause of potential cloud events, and finally give 
                    the most likely root cause (only one). Do not give results beyond the four failure types in the 
                    current system. The return failure often reports an error in the calling function due to information 
                    communication errors. However, the exception type cannot accurately locate the called function like return failure.And you should know that Return Failure typically relates to direct communication problems, such as failed service responses or incorrect information returned.And Exception generally involves broader service availability issues or unexpected conditions.
                    Please analyze this together with the data and the results given by Observable engineer.
                   """,
    description="Operation Engineer, responsible for referring to other experts' analysis and determining the root cause."
)
# 架构程序员
Architect_Expert_Agent = ConversableAgent(
    name='ArchitectExpert',
    llm_config=config_list,
    human_input_mode = "ALWAYS",
    system_message="""
                    # ROLE #
                    You are an architecture expert. Understand the specific architecture of the current system.
                    
                    #############
                    
                    # OBJECTIVE #
                    You are responsible for providing the current specific architecture information for other 
                    participants to analyze.Please analyze this together with the data and the results given by 
                    Observable engineer.
                    
                    #############
                    
                    # SKILLS #
                    The current system is a microservice train ticketing system, in which potential fault types include 
                    return, exception, network delay, cpu content. There are 41 microservices in the system.
                   """,
    description="Architecture Expert, provides system architecture related knowledge for other participants to analyze."
)

# 系统底层专家
System_Expert_Agent = ConversableAgent(
    name='SystemExpert',
    llm_config=config_list,
    human_input_mode = "ALWAYS",
    system_message="""
                    # ROLE #
                    You are a system expert. 
                    
                    #############
                    
                    # OBJECTIVE #
                    You are responsible for analyzing the CPU, return failure and exception related faults in the 
                    current system. If you think the current fault is not related to the content you are responsible for
                    analyzing, please explain. Please analyze this together with the data and the results given by Observable engineer. 

                    #############
                    
                    ### SKILLS #
                    You have extensive knowledge of system troubleshooting. Please focus on abnormal data related to CPU
                    and exception.
                   """,
    description="System expert,provide system resource error analysis for Operation Engineers to analyze."
)

# 网络专家
NetWork_Expert_Agent = ConversableAgent(
    name='NetWorkExpert',
    llm_config=config_list,
    human_input_mode = "ALWAYS",
    system_message="""
                    # ROLE #
                    As a network expert in cloud service abnormal events, your expertise is crucial to network and 
                    communication issues. 
                    
                    #############
                    
                    # OBJECTIVE #
                    You are responsible for analyzing network-related failures. If you think the current failure is not 
                    related to the content you are responsible for analyzing, please explain. Please analyze this 
                    together with the data and the results given by Observable engineer
                    
                    #############
                    
                    # SKILLS #
                    You have extensive knowledge of network delay troubleshooting. Please focus on abnormal data related
                    to the network delay.
                   """,
    description='Network expert, provide network fault analysis for Operation Engineers to analyze.'
)

# 数据观测人员 负责获取当前相关数据
Observable_engineer_agent = ConversableAgent(
    name='Observable_engineer_agent',
    llm_config=config_list,
    system_message="""
                    # CONTEXT #
                    This system is a cloud service train ticket sales system. I have a dataset of information of every 
                    fault. There are three files in the dataset: log, metric, and trace. 
                    The log file records the data items TimeUnixNano, TraceID, SpanID, Log, and the metric file records 
                    TimeStamp, PodName, CpuUsageRate(%), MemoryUsageRate(%), SyscallRead, SyscallWrite, 
                    NetworkReceiveBytes, NetworkTransmitBytes, PodClientLatencyP90(s), PodServerLatencyP90(s), 
                    PodClientLatencyP95(s), PodServerLatencyP95(s), PodClientLatencyP99(s), PodServerLatencyP99(s), 
                    PodWorkload(Ops), PodSuccessRate(%), NodeCpuUsageRate(%), NodeMemoryUsageRate(%), 
                    NodeNetworkReceiveBytes data items, and the trace file records StartTimeUnixNano, EndTimeUnixNano,
                    Duration, TraceID, SpanID, ParentID, PodName, OperationName.
                    Existing fault types include return,exception,network delay, cpu content. 
                    
                    #############
                    
                    # ROLE #
                    You are a useful data observable engineer who helps obtain relevant anomaly data from current failures. 
                    
                    #############
                    
                    # OBJECTIVE #
                    I would like you to use this dataset to perform anomaly analysis using this step-by-step process, not code:
                    1. You need to analyze the acquired data and generate a data table with anomalous data items, which must be within 150 to 180 words.
                    2. You need to call the alldata tool once.
                    3. Identify anomalous data points that deviate from the norm based on one or more column values.
                   """,
    description='Observable engineer, Obtain current abnormal data and display it for analysis by operation and maintenance personnel.',
)

# RAG,可使用私有历史数据测试
RAG_user_proxy_agent = RetrieveUserProxyAgent(
    name="RAG_Assistant",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": [
            "private/CMCC_fault_rag"
        ],
        "vector_db": "pgvector",
        "collection_name": "autogen_docs",
        "db_config": {
            "connection_string": "postgresql://test:abcd1234@localhost:5432/vectordb",
        },
        "custom_text_types": ["mdx"],
        "chunk_token_size": 2000,
        "model": "text-embedding-3-small",
        "get_or_create": True,
    },
    code_execution_config=False,
)

# 赋予数据观测人员调用函数获取数据的能力
register_function(
    alldata,
    caller=Observable_engineer_agent,  # The assistant agent can suggest calls to the calculator.
    executor=Operator,  # The user proxy agent can execute the calculator calls.
    name="data",  # By default, the function name is used as the tool name.
    description="A useful related data tool",  # A description of the tool.
)
# Group_chat = GroupChat(
#     messages=[],
#     agents=[RAG_user_proxy_agent, Operation_Engineer_Agent, Observable_engineer_agent, Operator,
#              NetWork_Expert_Agent, Architect_Expert_Agent, System_Expert_Agent],
#     send_introductions=True,
#     max_round=20,
# )
Group_chat = GroupChat(
    messages=[],
    agents=[User_proxy, Operation_Engineer_Agent, Observable_engineer_agent, Operator,
             NetWork_Expert_Agent, Architect_Expert_Agent, System_Expert_Agent],
    send_introductions=True,
    max_round=20,
)
Group_chat_manager = GroupChatManager(
    groupchat=Group_chat,
    llm_config=config_list,
)

# llm_lingua = LLMLingua()
# text_compressor = TextMessageCompressor(text_compressor=llm_lingua)
# context_handling = transform_messages.TransformMessages(transforms=[text_compressor])

# context_handling.add_to_agent(Operation_Engineer_Agent)
# context_handling.add_to_agent(Architect_Expert_Agent)
# context_handling.add_to_agent(Observable_engineer_agent)
# context_handling.add_to_agent(NetWork_Expert_Agent)
