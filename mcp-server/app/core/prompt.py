def build_prompt(message: str, history: list) -> str:
    prompt = "You are a helpful assistant.\n"
    for item in history:
        prompt += f"{item['role']}: {item['content']}\n"
    prompt += "Assistant:"
    return prompt
