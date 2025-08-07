from django.db import models


class LLMProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(blank=True)
    api_key = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name
