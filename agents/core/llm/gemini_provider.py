import json
import os
from typing import AsyncGenerator, Type, TypeVar
import httpx
from pydantic import BaseModel
from agents.core.llm.base_provider import ModelProvider

T = TypeVar("T", bound=BaseModel)


class GeminiProvider(ModelProvider):
    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gemini-1.5-flash",
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate(self, prompt: str, system: str | None = None) -> str:
        if not self.api_key:
            raise ValueError("Gemini API key is missing. Set GEMINI_API_KEY environment variable.")

        url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"

        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": f"System Instructions: {system}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": 0.2},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def structured_generate(self, prompt: str, schema: Type[T], system: str | None = None) -> T:
        schema_json = json.dumps(schema.model_json_schema())
        augmented_prompt = f"{prompt}\n\nRespond ONLY with a valid JSON object strictly matching this schema:\n{schema_json}"
        raw_text = await self.generate(augmented_prompt, system=system)
        clean_json = raw_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.removeprefix("```json").removesuffix("```").strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json.removeprefix("```").removesuffix("```").strip()
        data = json.loads(clean_json)
        return schema.model_validate(data)

    async def stream(self, prompt: str, system: str | None = None) -> AsyncGenerator[str, None]:
        result = await self.generate(prompt, system=system)
        yield result
