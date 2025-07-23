from datetime import datetime

def handle_with_tools(message: str) -> str | None:
    if "time" in message.lower():
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    return None
