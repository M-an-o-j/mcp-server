from core.context import ChatContext
from core.prompt import build_prompt
from core.llm import call_llm
from core.tools import handle_with_tools

context = ChatContext()

async def dispatch_message(message: str) -> str:
    context.add("user", message)

    # Check if message can be handled by tools
    tool_response = handle_with_tools(message)
    if tool_response:
        context.add("assistant", tool_response)
        return tool_response

    # Generate prompt and get LLM response
    prompt = build_prompt(message, context.get())
    llm_response = await call_llm(prompt)

    context.add("assistant", llm_response)
    return llm_response
