from __future__ import annotations

from typing import Any

import requests

from .base import LLMProvider


class BailianProvider(LLMProvider):
    """Provider for Alibaba Cloud's 百炼 (Bailian) service."""

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def chat(self, prompt: str, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'https://dashscope.aliyuncs.com'}/api/v1/chat/completions"
        payload = {"input": {"messages": [{"role": "user", "content": prompt}]}}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()

    def generate_image(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'https://dashscope.aliyuncs.com'}/api/v1/images/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def generate_video(self, prompt: str, **kwargs: Any) -> bytes:
        url = f"{self.base_url or 'https://dashscope.aliyuncs.com'}/api/v1/videos/generations"
        payload = {"prompt": prompt}
        payload.update(kwargs)
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.content

    def analyze_media(self, media: bytes, **kwargs: Any) -> Any:
        url = f"{self.base_url or 'https://dashscope.aliyuncs.com'}/api/v1/media/analyze"
        files = {"media": media}
        resp = requests.post(url, files=files, headers=self._headers(), timeout=kwargs.get("timeout", 30))
        resp.raise_for_status()
        return resp.json()
