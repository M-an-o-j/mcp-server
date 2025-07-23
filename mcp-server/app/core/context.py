# class ChatContext:
#     def __init__(self):
#         self.history = []

#     def add(self, role: str, content: str):
#         self.history.append({"role": role, "content": content})

#     def get(self):
#         return self.history

import json
import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class RedisChatContext:
    def __init__(self, session_id:str):
        self.key = f"chat_context:{session_id}"

    async def add(self, role: str, content: str):
        message = {"role": role, "content": content}
        history = await self.get()
        history.append(message)
        await redis_client.set(self.key, json.dumps(history))

    async def get(self) -> list:
        data = await redis_client.get(self.key)
        return json.loads(data) if data else []

    async def clear(self):
        await redis_client.delete(self.key)
