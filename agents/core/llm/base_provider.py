from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ModelProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system: str | None = None) -> str:
        pass

    @abstractmethod
    async def structured_generate(self, prompt: str, schema: Type[T], system: str | None = None) -> T:
        pass

    @abstractmethod
    async def stream(self, prompt: str, system: str | None = None) -> AsyncGenerator[str, None]:
        pass


class MockModelProvider(ModelProvider):
    """
    Deterministic provider for automated testing and initial slice execution.
    Does not require external network requests or paid API tokens.
    """

    def __init__(self, mock_responses: dict[str, Any] | None = None):
        self.mock_responses = mock_responses or {}

    async def generate(self, prompt: str, system: str | None = None) -> str:
        for key, response in self.mock_responses.items():
            if key in prompt:
                return response
        return "Deterministic agent output for prompt."

    async def structured_generate(self, prompt: str, schema: Type[T], system: str | None = None) -> T:
        # If the schema has a construct or defaults, return a filled instance
        if hasattr(schema, "model_validate"):
            return schema.model_validate({})
        return schema()  # type: ignore

    async def stream(self, prompt: str, system: str | None = None) -> AsyncGenerator[str, None]:
        yield "Deterministic "
        yield "stream "
        yield "content."
