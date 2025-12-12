"""Configuration management with environment variable loading."""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Application configuration."""

    # LLM Provider selection
    llm_provider: Literal["openai", "grok", "gemini", "local"] = Field(
        default="local",
        description="LLM provider to use",
    )

    # Storage
    storage_path: Path = Field(
        default=Path.home() / ".caption_ai" / "segments.db",
        description="Path to SQLite database",
    )

    # OpenAI
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")

    # Grok
    grok_api_key: str | None = Field(default=None, description="Grok API key")

    # Gemini
    gemini_api_key: str | None = Field(default=None, description="Gemini API key")

    # Local Ollama
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama base URL",
    )
    ollama_model: str = Field(
        default="llama2",
        description="Ollama model name",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Config()

