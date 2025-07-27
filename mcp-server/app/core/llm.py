# core/llm.py
import os
from dotenv import load_dotenv
from google import generativeai as genai
from core.tools import get_time, tool_calls
import json
from google.protobuf.json_format import MessageToDict

load_dotenv()

class GeminiAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=[get_time]
        )


    async def call(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            if response.candidates:
                parts = response.candidates[0].content.parts
                if parts:
                    return parts
            return "[LLM Error] Empty response"
        except Exception as e:
            return f"[LLM Errorrr] {str(e)}"
        

agent = GeminiAgent()

async def call_llm(prompt: str) -> str:
    return await agent.call(prompt)