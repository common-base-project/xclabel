from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Abstract base class for language model providers."""

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") if base_url else ""

    @abstractmethod
    def chat(self, prompt: str, **kwargs: Any) -> Any:
        """Return a chat completion for the given prompt."""

    @abstractmethod
    def generate_image(self, prompt: str, **kwargs: Any) -> Any:
        """Return an image generated for the prompt."""

    @abstractmethod
    def generate_video(self, prompt: str, **kwargs: Any) -> Any:
        """Return a video generated for the prompt."""

    @abstractmethod
    def analyze_media(self, media: bytes, **kwargs: Any) -> Any:
        """Analyze the given media and return a description or metadata."""

