from datetime import datetime

def tool_calls(**kwargs) -> str | None:
    if "get_time" == kwargs["name"]:
        return get_time(kwargs["params"])

def handle_with_tools(message: str) -> str | None:
    if "elli" in message.lower():
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    return None

def get_time(location: str) -> str:
    """
    Returns the current UTC time for a given location.

    Note: This function does not actually convert time zones based on the location;
    it simply returns the current UTC time with the location name included in the string.

    Args:
        location (str): The name of the location to include in the response.

    Returns:
        str: A string containing the current UTC time and the specified location.
    """
    return f"The current time in {location} is {datetime.utcnow().isoformat()} UTC"

