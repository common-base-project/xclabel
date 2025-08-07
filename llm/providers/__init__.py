from .base import LLMProvider
from .openai import OpenAIProvider

PROVIDER_MAP = {
    'openai': OpenAIProvider,
}

def get_provider(provider_type: str, **kwargs) -> LLMProvider:
    """Return provider implementation by type."""
    cls = PROVIDER_MAP.get(provider_type.lower())
    if not cls:
        raise ValueError(f'Unsupported provider type: {provider_type}')
    return cls(**kwargs)
