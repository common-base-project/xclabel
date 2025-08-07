from __future__ import annotations

from typing import Any

import requests

from .base import LLMProvider


class VolcEngineProvider(LLMProvider):
    """Provider for the Volcano Engine (VolcEngine) API."""

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def chat(self, prompt: str, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'https://api.volcengine.com'}/chat/completions"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()

    def generate_image(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'https://api.volcengine.com'}/images/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def generate_video(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'https://api.volcengine.com'}/videos/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def analyze_media(self, media: bytes, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'https://api.volcengine.com'}/media/analyze"
        files = {"media": media}
        resp = requests.post(url, files=files, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()
