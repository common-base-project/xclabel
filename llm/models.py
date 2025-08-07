from django.db import models


class LLMProvider(models.Model):
    """Stores configuration for an external LLM provider."""
    name = models.CharField(max_length=100, verbose_name='名称')
    type = models.CharField(max_length=50, verbose_name='类型')
    base_url = models.CharField(max_length=200, blank=True, verbose_name='基础URL')
    api_key = models.CharField(max_length=200, blank=True, verbose_name='API密钥')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    extra = models.TextField(blank=True, verbose_name='额外配置')

    class Meta:
        db_table = 'xc_llm_provider'
        verbose_name = 'LLM Provider'
        verbose_name_plural = 'LLM Providers'
