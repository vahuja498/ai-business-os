import json
import os
from typing import AsyncGenerator, Type, TypeVar
import httpx
from pydantic import BaseModel
from agents.core.llm.base_provider import ModelProvider

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider(ModelProvider):
    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "claude-3-5-sonnet-20241022",
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.model_name = model_name
        self.base_url = "https://api.anthropic.com/v1"

    def _get_headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ValueError("Anthropic API key is missing. Set ANTHROPIC_API_KEY environment variable.")
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    async def generate(self, prompt: str, system: str | None = None) -> str:
        payload = {
            "model": self.model_name,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(f"{self.base_url}/messages", headers=self._get_headers(), json=payload)
            res.raise_for_status()
            data = res.json()
            return data["content"][0]["text"]

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
