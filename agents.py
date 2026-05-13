from autogen import AssistantAgent, UserProxyAgent
from autogen import ConversableAgent
from autogen import GroupChatManager
from autogen import GroupChat
from autogen import register_function
from autogen.coding import LocalCommandLineCodeExecutor

from utils.skills4gy import *
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

config_list = {
    "config_list": [
        {
            "model": "gpt-4o-2024-05-13",
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "timeout": 100,
            "cache_seed": None
        }
    ]
}

temp_dir = tempfile.TemporaryDirectory()

executor = LocalCommandLineCodeExecutor(
    timeout=10,
    work_dir=temp_dir.name,
)

Operator = ConversableAgent(
    name="Operator",
    llm_config=False,
    code_execution_config={"executor": executor},
    description="Executes registered local tools. Can only be called by Observable_engineer_agent."
)

User_proxy = UserProxyAgent(
    name="User_proxy_agent",
    code_execution_config=False
)

EXPERT_JSON_SCHEMA = """
You must output valid JSON only.
Do not output markdown fences. Do not output explanations outside JSON.

{
  "expert_name": "<current expert name>",
  "root_cause_category": "network|resource|application|database|middleware|dependency|configuration|unknown",
  "service_location": {
    "dataset": "",
    "namespace": "",
    "service": "",
    "pod": "",
    "container": "",
    "node": "",
    "ip": "",
    "trace_service": "",
    "trace_span": ""
  },
  "summary": "",
  "confidence": 0.0,
  "evidence": [
    {
      "source_type": "metric|log|trace|architecture",
      "source_name": "",
      "abnormal_field": "",
      "abnormal_value": "",
      "reason": ""
    }
  ]
}
"""

FINAL_JSON_SCHEMA = """
You must output valid JSON only.
Do not output markdown fences. Do not output explanations outside JSON.

{
  "incident_id": "",
  "root_cause_category": "network|resource|application|database|middleware|dependency|configuration|unknown",
  "root_cause_detail": "",
  "service_location": {
    "dataset": "",
    "namespace": "",
    "service": "",
    "pod": "",
    "container": "",
    "node": "",
    "ip": "",
    "trace_service": "",
    "trace_span": ""
  },
  "affected_service": "",
  "confidence": 0.0,
  "evidence": [
    {
      "source_type": "metric|log|trace|architecture",
      "source_name": "",
      "abnormal_field": "",
      "abnormal_value": "",
      "reason": ""
    }
  ],
  "expert_findings": [
    {
      "expert_name": "",
      "root_cause_category": "network|resource|application|database|middleware|dependency|configuration|unknown",
      "service_location": {
        "dataset": "",
        "namespace": "",
        "service": "",
        "pod": "",
        "container": "",
        "node": "",
        "ip": "",
        "trace_service": "",
        "trace_span": ""
      },
      "summary": "",
      "confidence": 0.0,
      "evidence": []
    }
  ]
}
"""

Operation_Engineer_Agent = ConversableAgent(
    name="OperationEngineer",
    llm_config=config_list,
    human_input_mode="NEVER",
    system_message=f"""
# OBJECTIVE
You are the final diagnosis agent.

# TASK
Collect expert opinions, compare evidence, and return a single final diagnosis in JSON.

# RULES
1. You must determine:
   - root_cause_category
   - service_location
2. service_location is mandatory:
   - Prefer pod/container/node if confirmed
   - Else return service
   - Else return trace_service / trace_span
   - Never leave the whole object empty if any service clue exists
3. If experts disagree, choose the one with strongest evidence and highest confidence.
4. If evidence is insufficient, use "unknown" but still provide the most likely service_location.
5. Output JSON only.

# OUTPUT
{FINAL_JSON_SCHEMA}
""",
    description="Final diagnosis agent responsible for outputting the final structured incident diagnosis."
)

Architect_Expert_Agent = ConversableAgent(
    name="ArchitectExpert",
    llm_config=config_list,
    human_input_mode="NEVER",
    system_message=f"""
# OBJECTIVE
You analyze architecture dependency, service topology, and deployment position.

# FOCUS
- infer service position from architecture
- identify upstream/downstream dependency failures
- supplement service, pod, node, ip, dependency chain

# IMPORTANT
You must explicitly provide:
- root_cause_category
- service_location
- evidence

# OUTPUT
{EXPERT_JSON_SCHEMA}
""",
    description="Architecture Expert."
)

Resource_Expert_Agent = ConversableAgent(
    name="ResourceExpert",
    llm_config=config_list,
    human_input_mode="NEVER",
    system_message=f"""
# OBJECTIVE
You analyze system resource related faults.

# FOCUS
- cpu / memory / node / pod / container resource exhaustion
- abnormal runtime behavior
- resource bottlenecks

# IMPORTANT
You must explicitly provide:
- root_cause_category
- service_location
- evidence

# OUTPUT
{EXPERT_JSON_SCHEMA}
""",
    description="Resource expert."
)

NetWork_Expert_Agent = ConversableAgent(
    name="NetWorkExpert",
    llm_config=config_list,
    human_input_mode="NEVER",
    system_message=f"""
# OBJECTIVE
You analyze network and service communication faults.

# FOCUS
- timeout
- connection reset
- DNS / routing
- inter-service communication failure
- network packet loss / high latency

# IMPORTANT
You must explicitly provide:
- root_cause_category
- service_location
- evidence

# OUTPUT
{EXPERT_JSON_SCHEMA}
""",
    description="Network expert."
)

Observable_engineer_agent = ConversableAgent(
    name="Observable_engineer_agent",
    llm_config=config_list,
    human_input_mode="NEVER",
    system_message="""
# OBJECTIVE
You are the observation agent.

# TASK
Provide abnormal observation data and service localization clues for experts.

# RULES
When you call tools:
1. Always return BOTH:
   - raw data
   - summarized anomalies

2. For summary, highlight:
   - abnormal field
   - abnormal value
   - related service / pod / node / trace_service if possible

3. Prefer structured evidence instead of raw logs

# RESPONSE
Return observation evidence that helps determine:
- root_cause_category
- service_location
""",
    description="Observation agent."
)

register_function(
    alldata,
    caller=Observable_engineer_agent,
    executor=Operator,
    name="data",
    description="Read all related fault data."
)

register_function(
    architectureData,
    caller=Observable_engineer_agent,
    executor=Operator,
    name="architecture_information",
    description="Read architecture information."
)

register_function(
    process_log_data,
    caller=Observable_engineer_agent,
    executor=Operator,
    name="log_data_processing",
    description="Read and process log data."
)

register_function(
    process_metric_data,
    caller=Observable_engineer_agent,
    executor=Operator,
    name="metric_data_processing",
    description="Read and process metric data."
)

register_function(
    process_trace_data,
    caller=Observable_engineer_agent,
    executor=Operator,
    name="trace_data_processing",
    description="Read and process trace data."
)

Group_chat = GroupChat(
    messages=[],
    agents=[
        User_proxy,
        Operation_Engineer_Agent,
        Observable_engineer_agent,
        Operator,
        NetWork_Expert_Agent,
        Architect_Expert_Agent,
        Resource_Expert_Agent,
    ],
    send_introductions=True,
    max_round=20,
)

Group_chat_manager = GroupChatManager(
    groupchat=Group_chat,
    llm_config=config_list,
)