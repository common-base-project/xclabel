from __future__ import annotations

from typing import Any

import requests

from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """Provider for the Ollama local inference server."""

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def chat(self, prompt: str, **kwargs: Any) -> Any:
        base = self.base_url or "http://localhost:11434"
        url = f"{base}/api/chat"
        payload = {
            "model": kwargs.get("model", "llama2"),
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update({k: v for k, v in kwargs.items() if k not in {"model"}})
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()

    def generate_image(self, prompt: str, **kwargs: Any) -> bytes:
        base = self.base_url or "http://localhost:11434"
        url = f"{base}/api/images"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def generate_video(self, prompt: str, **kwargs: Any) -> bytes:
        base = self.base_url or "http://localhost:11434"
        url = f"{base}/api/videos"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def analyze_media(self, media: bytes, **kwargs: Any) -> Any:
        base = self.base_url or "http://localhost:11434"
        url = f"{base}/api/media/analyze"
        files = {"media": media}
        resp = requests.post(url, files=files, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()
