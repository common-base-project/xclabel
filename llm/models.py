from django.db import models


class LLMProvider(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    base_url = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    extra = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'xc_llm_provider'
