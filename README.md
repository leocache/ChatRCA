# ChatRCA

> Enhancing Root Cause Analysis via LLM-based Multi-Agents with Human-in-the-Loop

ChatRCA is an advanced tool for root cause analysis of cloud events. It builds a multi-intelligent agent root cause analysis method with humans in the loop, simulating the collaborative model in real-world root cause analysis. Multiple domain experts (Architecture, Resource, Network) collaborate through a group chat, observe abnormal data, and produce a structured diagnosis with root cause category, service location, and evidence.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Multi-Agent Design](#multi-agent-design)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Datasets](#datasets)
- [Project Structure](#project-structure)
- [Output Format](#output-format)
- [Empirical Study](#empirical-study)
- [License](#license)

---

## Architecture Overview

```
User_proxy ──▶ GroupChatManager ──▶ OperationEngineer (final diagnosis)
                     │
                     ├── Observable_engineer ──▶ Operator (tool execution)
                     ├── ArchitectExpert
                     ├── ResourceExpert
                     └── NetWorkExpert
```

1. **User_proxy** initiates the chat with a fault description (time, affected service).
2. **Observable_engineer** calls registered tools to read and filter abnormal data (log/metric/trace) and architecture information.
3. **Domain Experts** (Architect / Resource / Network) analyze the observation data from their professional perspective, each producing a structured JSON finding.
4. **OperationEngineer** collects all expert findings, compares evidence and confidence, and outputs the final structured diagnosis.

---

## Multi-Agent Design

| Agent | Role | Key Behavior |
|:------|:-----|:-------------|
| **User_proxy_agent** | Human-in-the-loop | Initiates fault report, can intervene at any round |
| **Observable_engineer_agent** | Data observation | Reads fault data via tools, filters anomalies, provides structured evidence |
| **Operator** | Tool executor | Executes registered Python functions (code execution agent, no LLM) |
| **ArchitectExpert** | Architecture expert | Analyzes service topology, deployment position, upstream/downstream dependencies |
| **ResourceExpert** | Resource expert | Analyzes CPU/memory/node/pod exhaustion, runtime bottlenecks |
| **NetWorkExpert** | Network expert | Analyzes timeouts, connection resets, DNS/routing, inter-service communication failures |
| **OperationEngineer** | Final diagnosis | Synthesizes expert findings, resolves conflicts by evidence strength, outputs final JSON diagnosis |

### Registered Tools

The Observable_engineer_agent has the following tools registered (executed by Operator):

| Tool | Description |
|:-----|:-----------|
| `data` | Read all related fault data (log + metric + trace) |
| `architecture_information` | Read architecture dependency information for the target system |
| `log_data_processing` | Read and filter log data (extract ERROR entries) |
| `metric_data_processing` | Read and filter metric data (abnormal PodSuccessRate / NodeCpuUsageRate) |
| `trace_data_processing` | Read and filter trace data (slow spans exceeding duration threshold) |

---

## Quick Start

### Requirements

- Python > 3.10
- OpenAI API key (GPT-4o)

### Installation

```bash
git clone https://github.com/leocache/ChatRCA.git
cd ChatRCA
pip install -r requirements.txt
```

### Configure API Key

```bash
cp .env.example .env
# Edit .env and fill in your OpenAI API key
```

### Run ChatRCA

1. Select a fault instance in `config.yaml`:

```yaml
fault: fault_1
```

2. Run the main program:

```bash
python main.py
```

3. The system will start a multi-agent group chat. Example output:

```
User_proxy_agent (to chat_manager):

The current cloud system experienced a failure at 2023-01-29 09:25:39.
The current ts-basic-service service is affected. Please analyze the root cause.

--------------------------------------------------------------------------------

Next speaker: OperationEngineer

OperationEngineer (to chat_manager):

Let's proceed with the analysis step by step:
1. Observable Engineer - Please provide the current abnormal data.
2. NetWork Expert - Prepare to analyze network-related issues.
3. Architecture Expert - Be ready to provide architecture insights.
4. Resource Expert - Prepare to examine resource-related anomalies.

...
```

### Run on GAIA Dataset

Edit `main.py` to switch the entry function:

```python
if __name__ == '__main__':
    # run_TrainTicket_fault()
    run_GAIA_fault()
```

---

## Configuration

### config.yaml

| Field | Description | Example |
|:------|:------------|:--------|
| `fault` | Fault instance directory name under the dataset folder | `fault_1`, `F_6` |

### .env

| Variable | Description |
|:---------|:-----------|
| `OPENAI_API_KEY` | Your OpenAI API key (required for GPT-4o) |

### agents.py

The LLM model and group chat parameters can be configured in `agents.py`:

- `config_list` — model name, API key, timeout
- `Group_chat.max_round` — maximum conversation rounds (default: 20)
- `human_input_mode` — set to `"ALWAYS"` for human-in-the-loop, `"NEVER"` for fully autonomous

---

## Datasets

### D1: TrainTicket (Open Source)

An open-source dataset from the medium-sized case system **TrainTicket**. Contains **45 fault instances** covering real fault types: system resource exhaustion, network anomalies, application errors, etc.

- Location: `TrainTicket/fault_*/`
- Each fault folder contains:
  - `fault.txt` — fault injection source information (JSON format)
  - `log.csv` — log data before and after the fault
  - `metric.csv` — metric data before and after the fault
  - `trace.csv` — trace data before and after the fault

### D2: GAIA (Private)

A private dataset collected from a core system on a large enterprise cloud platform. Due to data security requirements, the raw data cannot be open-sourced. Pre-processed data is provided in the `GAIA/` directory.

- Location: `GAIA/F_*/`
- Data cleaning scripts: `GAIA_DataCleaning/`

### D3: PrivateFault (Private)

Additional private fault data stored in `PrivateFault/`, not open-sourced.

---

## Project Structure

```
ChatRCA/
├── main.py                  # Entry point: run_TrainTicket_fault() / run_GAIA_fault()
├── agents.py                # Multi-agent definitions, tool registration, group chat setup
├── schemas.py               # Pydantic schemas for structured diagnosis output
├── config.yaml              # Fault instance selection
├── .env.example             # API key template
├── requirements.txt         # Python dependencies
│
├── utils/                   # Utility modules
│   ├── __init__.py          # Package init, exposes get_fault_info, get_fault_type_census
│   ├── read_file.py         # File reading: YAML, CSV→Markdown, fault path resolution
│   ├── csv2md.py            # CSV to Markdown table converter
│   ├── filter_tools.py      # Data filters: error logs, abnormal metrics, slow traces
│   ├── location_tools.py    # Service location normalization and inference from pod names
│   ├── observation_summary.py # Summarize filtered data into structured evidence
│   ├── skills4tt.py         # Tools for TrainTicket dataset (registered as agent skills)
│   └── skills4gy.py         # Tools for GAIA dataset (registered as agent skills)
│
├── architecture/            # Architecture dependency documents
│   ├── TrainTicket.md       # TrainTicket microservice topology and dependencies
│   └── GAIA.md              # GAIA system architecture
│
├── TrainTicket/             # D1 dataset: 45 fault instances
│   ├── fault_1/
│   │   ├── fault.txt
│   │   ├── log.csv
│   │   ├── metric.csv
│   │   └── trace.csv
│   ├── fault_2/
│   └── ...
│
├── GAIA/                    # D2 dataset (pre-processed)
│   └── DataCleaning/        # Data cleaning scripts for GAIA
├── PrivateFault/            # D3 private fault data
│
├── empirical_study/         # Empirical research questionnaire responses
│   ├── Questionnaire_1.docx
│   └── ...
│
└── LICENSE                  # MIT License
```
---

## Empirical Study

The `empirical_study/` directory contains 20 questionnaire response files (`Questionnaire_1.docx` ~ `Questionnaire_20.docx`) from the empirical evaluation described in our paper. These questionnaires assess the effectiveness and usability of the ChatRCA approach from domain practitioners.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
