from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """Placeholder implementation for OpenAI compatible APIs."""

    def chat(self, messages, model: str = None, **kwargs):
        # In actual implementation, this would call OpenAI's API.
        return {
            'model': model or 'gpt-3.5-turbo',
            'messages': messages,
            'reply': 'mock response'
        }

    def generate_image(self, prompt: str, **kwargs):
        return {'prompt': prompt, 'url': ''}

    def generate_video(self, prompt: str, **kwargs):
        return {'prompt': prompt, 'url': ''}

    def analyze_media(self, file, task: str, **kwargs):
        return {'task': task, 'result': 'not implemented'}
