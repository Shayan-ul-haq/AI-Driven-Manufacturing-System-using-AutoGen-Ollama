# AI-Driven-Manufacturing-System-using-AutoGen-Ollama
This project implements an **AI‑driven flexible manufacturing cell** where intelligent agents behave like factory machines and managers. Instead of fixed logic, the system uses **LLM‑powered agents** (AutoGen + Ollama) to negotiate processing times and autonomously award a manufacturing contract.

---

## 1. Concept: AI‑Driven Manufacturing

In traditional factories, humans decide:

- Which machine is free  
- Which machine is fast  
- How long a job will take  
- Who should get the order  

In this **AI‑driven project**, these decisions are made by **LLM agents**:

- **Machine Agents** act like real machines (Drilling, Milling, etc.)
- **Order Manager Agent** behaves like a production planner
- They communicate in **natural language** and negotiate processing times

This demonstrates how **AI agents can automate scheduling and decision‑making** in a smart factory.

---

## 2. Tech Stack

- Python  
- AutoGen (pyautogen)  
- Ollama (local LLM server)  
- Local LLM model (llama3, mistral, phi3, etc.)

---

## 3. Phase 1 – LLM Configuration (Connecting AutoGen to Ollama)

```python
import autogen

llm_config = {
    "config_list": [
        {
            "model": "llama3",
            "api_key": "ollama",
            "base_url": "http://127.0.0.1:11434/v1",
        }
    ],
    "temperature": 0.7,
}
This connects AutoGen to the local LLM running inside Ollama.

4. Phase 2 – Agent Personas (Machine & Order Manager)
python
from autogen import AssistantAgent, UserProxyAgent

# Machine Agent
machine_agent = AssistantAgent(
    name="Milling_Machine",
    system_message=(
        "You are a Milling Machine in a manufacturing plant. "
        "When you receive a job request, reply with a processing time "
        "between 10 and 50 minutes."
    ),
    llm_config=llm_config,
)

# Order Manager Agent
order_agent = UserProxyAgent(
    name="Order_Manager",
    system_message=(
        "You are an order manager. Your goal is to get the best possible "
        "processing time from the available machines."
    ),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config=False,
)
5. Phase 3 – 1‑on‑1 Negotiation
python
order_agent.initiate_chat(
    machine_agent,
    message="I have an urgent order that requires milling. Can you take this job, and how long will it take?"
)
The machine responds with a time estimate.

6. Phase 4 – Multi‑Machine Group Chat
python
from autogen import GroupChat, GroupChatManager

drill_a = AssistantAgent(
    name="Drill_A",
    system_message="You are an older, slower drilling machine.",
    llm_config=llm_config,
)

drill_b = AssistantAgent(
    name="Drill_B",
    system_message="You are a newer, faster but busy drilling machine.",
    llm_config=llm_config,
)

groupchat = GroupChat(
    agents=[order_agent, drill_a, drill_b],
    messages=[],
    max_round=5,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

order_agent.initiate_chat(
    manager,
    message="I need a drilling job done. Each machine should propose a processing time. Who can do it the fastest?"
)
7. Phase 5 – AI‑Driven Contract Net (LLM Decision Making)
python
order_agent = UserProxyAgent(
    name="Order_Manager",
    system_message=(
        "You are an order manager. Ask all machines for processing times. "
        "Wait for all machines to respond. Compare the times in their messages. "
        "Reply to the machine with the lowest time saying 'CONTRACT AWARDED'. "
        "Reply 'REJECTED' to the others. Then output 'TERMINATE'."
    ),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config=False,
)
