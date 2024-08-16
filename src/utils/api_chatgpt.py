import redis
import json
import openai
from typing import Dict, List
from PIL import Image
from io import BytesIO
import config
import os
import aiofiles
import base64

from openai import AsyncOpenAI


class OpenAIHelper:
    def __init__(self, api_key: str, model: str, max_tokens: int = 100):
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        self.max_tokens = max_tokens
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    def _get_context_key(self, user_id: int) -> str:
        return f"contexts:{user_id}"

    async def clear_context(self, user_id: int):
        """Очищает контекст для конкретного пользователя."""
        self.redis_client.delete(self._get_context_key(user_id))

        

    async def add_message(self, user_id: int, role: str, content: str):
        """Добавляет сообщение в контекст для конкретного пользователя."""
        context_key = self._get_context_key(user_id)
        context = self.redis_client.get(context_key)
        if context is None:
            context = []
        else:
            context = json.loads(context)
        context.append({"role": role, "content": content})
        self.redis_client.set(context_key, json.dumps(context))
        await self._write_to_file(user_id, role, content)

    async def prompts(self, user_id: int, prompt: str) -> str:
        """Отправляет запрос в модель GPT и возвращает ответ для конкретного пользователя."""
        context_key = self._get_context_key(user_id)
        context = self.redis_client.get(context_key)
        if context is None:
            context = []
            await self.add_message(user_id, role='system', content=config.chatgpt_training_formating)
        else:
            context = json.loads(context)
        context.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=context,
            max_tokens=self.max_tokens
        )
        message = response.choices[0].message.content
        context.append({"role": "assistant", "content": message})
        self.redis_client.set(context_key, json.dumps(context))
        return message


    async def interpret_image(self, user_id: int, image_file: BytesIO, prompt: str) -> str:
        """Интерпретирует изображение с помощью модели GPT."""
        # Читаем и кодируем изображение в base64
        buffer = BytesIO()
        buffer.write(image_file.getbuffer())
        buffer.seek(0)
        base64_image = base64.b64encode(buffer.read()).decode('utf-8')

        context_key = self._get_context_key(user_id)
        context = self.redis_client.get(context_key)
        if context is None:
            context = [{"role": "system", "content": "You are a helpful assistant."}]
        else:
            context = json.loads(context)

        context.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "low"
                },
            },]
        }) 

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=context,
            max_tokens=self.max_tokens
        )

        message = response.choices[0].message.content
        context.append({"role": "assistant", "content": message})
        self.redis_client.set(context_key, json.dumps(context))
        await self._write_to_file(user_id, "image_prompt", prompt)
        await self._write_to_file(user_id, "image_response", message)
        return message

    async def _write_to_file(self, user_id: int, role: str, content: str):
        """Записывает запросы в файл."""
        file_path = f"users/user_data_{user_id}.json"
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Записываем данные в файл
        async with aiofiles.open(file_path, mode='a') as file:
            entry = {
                "role": role,
                "content": content
            }
            await file.write(json.dumps(entry, ensure_ascii=False, indent=4) + '\n')

openai_helper = OpenAIHelper(api_key=config.OPENAI_API_KEY, model=config.OPEN_AI_MODEL, max_tokens=2000)
