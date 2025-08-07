"""OpenAI compatible LLM provider.

This module exposes a thin wrapper around OpenAI's HTTP API.  It is
implemented with ``requests`` so it can talk to any OpenAI compatible
endpoint (including self‑hosted or proxy services).  The provider supports
chat completions, image and video generation and the generic
``/responses`` endpoint used for analysis or other multimodal operations.

The API key and base URL are read from environment variables
``OPENAI_API_KEY`` and ``OPENAI_BASE_URL``.  They can also be supplied
explicitly when instantiating :class:`OpenAIProvider`.

Streaming responses are returned as generators yielding the parsed JSON
objects from each event chunk.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Generator, Optional
import json
import os

import requests


@dataclass
class OpenAIProvider:
    """Simple wrapper for OpenAI compatible APIs."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None

    def __post_init__(self) -> None:  # noqa: D401 - short description
        self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = self.base_url or os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")

    # ------------------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _request(
        self, endpoint: str, payload: Dict[str, Any], stream: bool = False
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self._headers(), json=payload, stream=stream)
        response.raise_for_status()
        if stream:
            return self._stream(response)
        return response.json()

    # ------------------------------------------------------------------
    def _stream(self, response: requests.Response) -> Generator[Dict[str, Any], None, None]:
        for line in response.iter_lines():
            if not line:
                continue
            text = line.decode("utf-8")
            if text.startswith("data: "):
                text = text[6:]
            if text.strip() == "[DONE]":
                break
            yield json.loads(text)

    # ------------------------------------------------------------------
    def chat(
        self,
        messages: Iterable[Dict[str, str]],
        model: str,
        **kwargs: Any,
    ) -> Any:
        """Call the ``/chat/completions`` endpoint.

        Set ``stream=True`` in ``kwargs`` to receive a generator yielding
        events for streamed responses.
        """
        payload: Dict[str, Any] = {"model": model, "messages": list(messages)}
        payload.update(kwargs)
        stream = bool(payload.get("stream"))
        return self._request("chat/completions", payload, stream=stream)

    def image(self, prompt: str, model: str, **kwargs: Any) -> Any:
        """Call the ``/images/generations`` endpoint."""
        payload: Dict[str, Any] = {"model": model, "prompt": prompt}
        payload.update(kwargs)
        return self._request("images/generations", payload)

    def video(self, prompt: str, model: str, **kwargs: Any) -> Any:
        """Call the ``/videos/generations`` endpoint."""
        payload: Dict[str, Any] = {"model": model, "prompt": prompt}
        payload.update(kwargs)
        return self._request("videos/generations", payload)

    def analyze(self, input: Any, model: str, **kwargs: Any) -> Any:
        """Call the ``/responses`` endpoint for generic analysis."""
        payload: Dict[str, Any] = {"model": model, "input": input}
        payload.update(kwargs)
        stream = bool(payload.get("stream"))
        return self._request("responses", payload, stream=stream)
