from django.test import TestCase
from .providers import get_provider


class ProviderFactoryTests(TestCase):
    def test_get_unknown_provider(self):
        with self.assertRaises(ValueError):
            get_provider('unknown')

    def test_get_openai_provider(self):
        provider = get_provider('openai')
        from .providers.openai import OpenAIProvider
        self.assertIsInstance(provider, OpenAIProvider)
