from __future__ import annotations

from django.db import models
from llm.models import LLMProvider


class Agent(models.Model):
    """Represents a configurable agent bound to an LLM provider."""

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    provider = models.ForeignKey(LLMProvider, on_delete=models.CASCADE, related_name='agents')
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'xc_agent'


class AgentSession(models.Model):
    """Stores conversation history for an agent instance."""

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.CharField(max_length=100, unique=True)
    messages = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'xc_agent_session'


class WorkflowSession(models.Model):
    """Tracks workflow execution nodes and their results."""

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='workflows')
    session_id = models.CharField(max_length=100, unique=True)
    nodes = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'xc_agent_workflow'
