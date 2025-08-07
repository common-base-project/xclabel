from __future__ import annotations

from typing import Any

import requests

from .base import LLMProvider


class VLLMProvider(LLMProvider):
    """Provider for a vLLM server."""

    def _headers(self) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        return headers

    def chat(self, prompt: str, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'http://localhost:8000'}/v1/chat/completions"
        payload = {"messages": [{"role": "user", "content": prompt}]}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()

    def generate_image(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'http://localhost:8000'}/v1/images/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def generate_video(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'http://localhost:8000'}/v1/videos/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def analyze_media(self, media: bytes, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'http://localhost:8000'}/v1/media/analyze"
        files = {"media": media}
        resp = requests.post(url, files=files, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()
