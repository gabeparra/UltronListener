"""Local Ollama client via HTTP."""

import httpx

from caption_ai.config import config
from caption_ai.llm.base import LLMClient, LLMReply


class LocalOllamaClient(LLMClient):
    """Local Ollama client implementation."""

    def __init__(self) -> None:
        """Initialize Ollama client."""
        self.base_url = config.ollama_base_url
        self.model = config.ollama_model

    async def complete(self, prompt: str) -> LLMReply:
        """Complete prompt using local Ollama API."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content", "")
                return LLMReply(
                    content=content,
                    model=self.model,
                )
        except httpx.RequestError as e:
            return LLMReply(
                content=f"Error connecting to Ollama: {e}. "
                f"Make sure Ollama is running at {self.base_url}",
            )
        except Exception as e:
            return LLMReply(
                content=f"Error calling Ollama: {e}",
            )

