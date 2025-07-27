# core/llm.py
import os
from dotenv import load_dotenv
from google import generativeai as genai
from core.tools import get_time, tool_calls
import json
from google.protobuf.json_format import MessageToDict

load_dotenv()


# genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_time]  # Pass the tool list here
)

async def call_llm(prompt: str) -> str:
    try:
        response = await model.generate_content_async(prompt)
        if response.candidates:
            parts = response.candidates[0].content.parts
            for part in parts:
                if hasattr(part, 'function_call'):
                    print(part)
                    message_dict = dict(part.function_call.args)
                    print(message_dict, "dictt")
                    tool_res = tool_calls(name=part.function_call.name, params=message_dict["location"])
                    return tool_res
                elif hasattr(part, 'text'):
                    return part.text.strip()

        return "[LLM Error] Empty response"
    except Exception as e:
        return f"[LLM Errorrr] {str(e)}"

class GeminiAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=[get_time]
        )

    async def call(self):
        response = await self.model.generate_content_async(
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                max_output_tokens=1000
            )
        )

        if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        function_call = part.function_call
                        tool_name = function_call.name
                        tool_args = {k: v for k, v in function_call.args.items()} # Convert to dict

                        # --- MODIFIED: Return the suggested function call as a string ---
                        suggestion = f"Suggested Tool Call: {tool_name}({json.dumps(tool_args)})"
                        print(f"\n[Agent Suggestion] {suggestion}")

                        # Update chat history with the model's suggestion (optional, but good for context)
                        # Here, we'll add the model's *original* response part to history
                        self.chat_history.append({"role": "model", "parts": [part]})
                        return suggestion

                # If no tool call, it's a direct text response from Gemini
                if response.text:
                    self.chat_history.append({"role": "model", "parts": [response.text]})
                    return response.text
                else:
                    return "[Agent Error] No text or tool call in response."