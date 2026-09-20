import json
import os
from typing import AsyncGenerator, Type, TypeVar
import httpx
from pydantic import BaseModel
from agents.core.llm.base_provider import ModelProvider

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(ModelProvider):
    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")

    def _get_headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ValueError("OpenAI API key is missing. Set OPENAI_API_KEY environment variable.")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def generate(self, prompt: str, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.3,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(f"{self.base_url}/chat/completions", headers=self._get_headers(), json=payload)
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]

    async def structured_generate(self, prompt: str, schema: Type[T], system: str | None = None) -> T:
        schema_json = json.dumps(schema.model_json_schema())
        augmented_prompt = (
            f"{prompt}\n\nRespond ONLY with a valid JSON object strictly matching this schema:\n{schema_json}"
        )
        raw_text = await self.generate(augmented_prompt, system=system)
        # Parse JSON from response
        clean_json = raw_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.removeprefix("```json").removesuffix("```").strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json.removeprefix("```").removesuffix("```").strip()
        data = json.loads(clean_json)
        return schema.model_validate(data)

    async def stream(self, prompt: str, system: str | None = None) -> AsyncGenerator[str, None]:
        # Simple fallback stream
        result = await self.generate(prompt, system=system)
        yield result
