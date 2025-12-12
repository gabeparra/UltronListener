"""Base LLM client interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMReply:
    """Response from LLM."""

    content: str
    model: str | None = None
    tokens_used: int | None = None


class LLMClient(ABC):
    """Base interface for LLM clients."""

    @abstractmethod
    async def complete(self, prompt: str) -> LLMReply:
        """Complete a prompt and return response."""
        pass

