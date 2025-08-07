class LLMProvider:
    """Base class for LLM providers."""

    def __init__(self, base_url: str = None, api_key: str = None, **kwargs):
        self.base_url = base_url
        self.api_key = api_key

    def chat(self, messages, model: str = None, **kwargs):
        raise NotImplementedError

    def generate_image(self, prompt: str, **kwargs):
        raise NotImplementedError

    def generate_video(self, prompt: str, **kwargs):
        raise NotImplementedError

    def analyze_media(self, file, task: str, **kwargs):
        raise NotImplementedError
