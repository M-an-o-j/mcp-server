from core.context import  RedisChatContext
from core.prompt import build_prompt
from core.llm import call_llm
from core.tools import handle_with_tools

async def dispatch_message(message: str, session_id: str = "default_session") -> str:
    context = RedisChatContext(session_id)

    await context.add("user", message)

    # Check if message can be handled by tools
    tool_response = handle_with_tools(message)
    if tool_response:
        await context.add("assistant", tool_response)
        return tool_response

    # Generate prompt and get LLM response
    history = await context.get()
    prompt = build_prompt(message, history)
    llm_response = await call_llm(prompt)
    # print(llm_response.name,"response")
    await context.clear()
    # await context.add("assistant", llm_response)
    return llm_response
