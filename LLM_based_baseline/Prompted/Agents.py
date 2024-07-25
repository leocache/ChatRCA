from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import os


load_dotenv()
#, "base_url": os.environ.get("OPENAI_API_BASE")
config_list = {"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY"), "timeout": 100, "cache_seed": None}]}

User_proxy = UserProxyAgent(
    name='User_proxy_agent',
    code_execution_config=False
)

Assistant = AssistantAgent(
    name='Assistant',
    llm_config=config_list,
)