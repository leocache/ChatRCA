# ChatRCA

This repository is a basic implementation of the method proposed in our paper "ChatRCA: Enhancing Root Cause Analysis via LLM based Multi-Agents with Human-in-the-Loop".  In addition, we also implemented the non-open source baseline method.

|         File Directory          |                          Introduce                           |
| :-----------------------------: | :----------------------------------------------------------: |
|         Root directory          | The Root directory stores the basic ChatRCA method we implemented. |
| LLM_based_baseline/GPT-4o_Embed | The directory corresponds to the baseline method "GPT-4o_Embed" that we implemented in the paper. |
|   LLM_based_baseline/Prompted   | The directory corresponds to the baseline method "GPT-3.5 Turbo/4o Prompted" that we implemented in the paper. |

## Description

ChatRCA is an advanced tool for root cause analysis of cloud events. It builds a multi-intelligent agent root cause analysis method with humans in the loop, simulating the collaborative model in real-world root cause analysis. ChatRCA provides a new path for root cause analysis.

## Quick Start

### Requirements

We recommend using Python version > 3.10 for this project. Other dependencies are listed in the `requirements.txt` file.

### Preparatory steps

1. Run the following command to clone our project:

```
git clone https://github.com/leocache/ChatRCA.git
```

2. Navigate to the project root directory.

3. Install the project dependencies:

```
pip install -r requirements.txt
```

4. Rename `.env.example` to `.env` . Then fill in your OpenAI api_key in the `.env` file.

### Running ChatRCA

1. Operation and maintenance data is indexed by faults and stored in TrainTicket/fault_* files. You need to modify the fault option in the config.yaml file as the data source for ChatRCA to read.

   ```
   fault: fault_1
   ```

2. Next, execute the "main.py" file directly.

   We can find that the "User_proxy_agent" will start a system dialogue, in which it will tell the system what has happened. The system will then read data and analyze the failure according to the logic we designed. During this period, humans can intervene at any time, which is what we call Human-in-the-Loop in our paper.

```
User_proxy_agent (to chat_manager):

The current cloud system experienced a failure at 2023-01-29 09:25:39. The current ts-basic-service service is affected. Please analyze the root cause.

--------------------------------------------------------------------------------

Next speaker: OperationEngineer

Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: 

>>>>>>>> NO HUMAN INPUT RECEIVED.

>>>>>>>> USING AUTO REPLY...
OperationEngineer (to chat_manager):

Certainly, let's proceed with the analysis step by step:
1. **Observable Engineer** - Please provide the current abnormal data related to the failure for further analysis.
2. **NetWork Expert** - Prepare to analyze network-related issues such as network delays.
3. **Architecture Expert** - Be ready to provide any pertinent system architecture-related insights.
4. **System Expert** - Prepare to examine system resource-related anomalies or faults, especially those related to CPU.

We'll start with the data. Observable Engineer, please proceed and obtain the current abnormal data.
--------------------------------------------------------------------------------
……
```

## Dataset

We used two datasets. 

D1 is an open source dataset from the well-known medium-sized case system Train ticket. The dataset contains 45 fault instances, and the fault types involve real faults such as system resources, networks, and anomalies.
D2 is a private dataset. We collected real cloud events and anomaly data from a core system on a large enterprise cloud platform. The details are introduced in our paper. Due to the enterprise's data security requirements, we cannot open source the dataset for the time being.

We organized the D1 dataset, mainly by indexing it by fault, and storing it in the [TrainTicket](/TrainTicket)/fault_* directory. Each folder contains four files, namely **fault.txt**, **log.csv**, **trace.csv,** and **metric.csv.** Among them, fault.txt is the original information of fault injection, and the other three files are the operation and maintenance data before and after the fault injection. 

## Project Structure

```
.
│  LICENSE
│  README.md
│  .env.example: Api_key configuration file.
│  config.yaml: Data Source Configuration File.
│  Agents.py: ChatRCA agents definition.
│  CSV2md.py: Csv table processing tool.
│  main.py: ChatRCA main program.
│  Tooluse.py: Data collection and processing tools for agents.          
├─TrainTicket
│  ├─fault_1
│  │      fault.txt: Fault injection source information.  
│  │      log.csv: Log information before and after the failure.
│  │      metric.csv: Metric information before and after the failure
│  │      trace.csv: Trace information before and after the failure      
│  ├─fault_2
│  ├─fault_3
│  ├─fault_4          
│  requirements.txt  
├─LLM_based_baseline: Baseline method implementation.
│  ├─GPT-4o_Embed: Baseline method "GPT-4o_Embed" implementation.
│  │  │  .env.example
│  │  │  config.yaml
│  │  │  CSV2md.py
│  │  │  RAG.py
│  │  │  rag_knowledge.md
│  │  │  requirements.txt
│  │  │  Tooluse.py
│  └─Prompted: Baseline method "Prompted" implementation.
│      │  .env.example
│      │  Agents.py
│      │  config.yaml
│      │  CSV2md.py
│      │  main.py
│      │  requirements.txt
│      │  Tooluse.py
│  .gitignore


```

