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