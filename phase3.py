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

# Task 4: Two Machine Agents
drill_a = autogen.AssistantAgent(
    name="Drill_A",
    system_message=(
        "You are Drill_A, an older and slower drilling machine in a manufacturing plant. "
        "When asked for a bid, provide a processing time between 30 and 50 minutes."
    ),
    llm_config=llm_config,
)

drill_b = autogen.AssistantAgent(
    name="Drill_B",
    system_message=(
        "You are Drill_B, a fast but busy drilling machine. "
        "When asked for a bid, provide a processing time between 15 and 25 minutes."
    ),
    llm_config=llm_config,
)

# Task 5: Order Manager with termination
order_agent = autogen.UserProxyAgent(
    name="Order_Manager",
    system_message=(
        "You are an order manager. Ask the machines for processing times. "
        "Wait for all machines to respond. Compare the times provided in their text. "
        "Reply directly to the machine with the lowest time stating 'CONTRACT AWARDED'. "
        "Say 'REJECTED' to the others. Then output 'TERMINATE'."
    ),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

# Task 4: Group Chat setup
groupchat = autogen.GroupChat(
    agents=[order_agent, drill_a, drill_b],
    messages=[],
    max_round=6,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# Task 4: Initiate from Order_Manager to manager
order_agent.initiate_chat(
    manager,
    message="I need a drilling job done. Who can do it the fastest? Please both provide your best time estimate."
)