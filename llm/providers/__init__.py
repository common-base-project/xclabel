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
    "openai": OpenAIProvider,
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


def get_provider(provider_type: str, **kwargs) -> LLMProvider:
    """Return an initialized provider implementation.

    Args:
        provider_type: The identifier for the provider implementation.
        **kwargs: Additional keyword arguments passed to the provider constructor
            such as ``api_key`` or ``base_url``.

    Raises:
        ValueError: If ``provider_type`` is not a supported provider.

    Returns:
        An instance of :class:`LLMProvider`.
    """

    try:
        provider_cls = PROVIDER_MAP[provider_type]
    except KeyError as exc:
        raise ValueError(f"Unknown provider type: {provider_type}") from exc
    return provider_cls(**kwargs)
