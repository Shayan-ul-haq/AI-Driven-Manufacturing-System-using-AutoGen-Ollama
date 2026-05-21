from autogen import AssistantAgent, UserProxyAgent

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

milling_agent = AssistantAgent(
    name="Milling_Machine",
    system_message=(
        "You are a Milling Machine in a manufacturing plant. "
        "When you receive a job request, reply with a proposed processing time "
        "between 10 and 50 minutes."
    ),
    llm_config=llm_config,
)

order_agent = UserProxyAgent(
    name="Order_Manager",
    system_message=(
        "You are a customer order manager. You need a Milling job done. "
        "Negotiate to get the best time."
    ),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config=False,
)

order_agent.initiate_chat(
    milling_agent,
    message="I have an urgent order that requires Milling. Can you take this job, and how long will it take?"
)