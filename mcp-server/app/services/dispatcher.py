from core.context import  RedisChatContext
from core.prompt import build_prompt
from core.llm import call_llm
from core.tools import handle_with_tools, tool_calls

async def dispatch_message(message: str, session_id: str = "default_session") -> str:
    context = RedisChatContext(session_id)

    await context.add("user", message)

    history = await context.get()
    prompt = build_prompt(message, history)
    llm_response = await call_llm(prompt)
    for part in llm_response:
        if hasattr(part, 'function_call'):
            message_dict = dict(part.function_call.args)
            tool_res = tool_calls(name=part.function_call.name, params=message_dict["location"])
            return tool_res
        elif hasattr(part, 'text'):
            return part.text.strip()
    # await context.clear()
    await context.add("assistant", llm_response)
    return llm_response
