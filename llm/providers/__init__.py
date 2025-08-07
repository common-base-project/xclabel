"""LLM provider implementations and factory utilities."""

from .base import LLMProvider
from .deepseek import DeepSeekProvider
from .volcengine import VolcEngineProvider
from .vllm import VLLMProvider
from .ollama import OllamaProvider
from .bailian import BailianProvider
from .openai import OpenAIProvider

PROVIDER_MAP = {
    "openai": OpenAIProvider,
    "deepseek": DeepSeekProvider,
    "volcengine": VolcEngineProvider,
    "vllm": VLLMProvider,
    "ollama": OllamaProvider,
    "bailian": BailianProvider,
}


def get_provider(name: str, **kwargs) -> LLMProvider:
    """Return an instance of the provider implementation.

    Parameters
    ----------
    name: str
        Provider type, e.g. ``openai`` or ``deepseek``.
    **kwargs:
        Keyword arguments passed to the provider constructor such as
        ``api_key`` or ``base_url``.

    Raises
    ------
    ValueError
        If the provider name is unknown.
    """

    cls = PROVIDER_MAP.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown provider: {name}")
    return cls(**kwargs)


__all__ = [
    "LLMProvider",
    "DeepSeekProvider",
    "VolcEngineProvider",
    "VLLMProvider",
    "OllamaProvider",
    "BailianProvider",
    "OpenAIProvider",
    "PROVIDER_MAP",
    "get_provider",
]
