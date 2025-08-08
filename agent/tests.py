import json

from django.test import TestCase, Client

from llm.models import LLMProvider
from .models import Agent


class AgentAPITests(TestCase):
    def setUp(self):
        self.provider = LLMProvider.objects.create(
            name='OpenAI', type='openai', api_key='test'
        )
        self.agent = Agent.objects.create(
            name='bot', type='chat', provider=self.provider, config={'model': 'gpt-3.5-turbo'}
        )
        self.client = Client()

    def test_chat_endpoint(self):
        resp = self.client.post(
            '/api/agent/chat',
            data=json.dumps({'agent_id': self.agent.id, 'message': 'hi'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('reply', data)
        self.assertEqual(len(data['messages']), 2)

    def test_workflow_execute(self):
        workflow = [{'id': 'step1', 'prompt': 'hello'}]
        resp = self.client.post(
            '/api/agent/workflow/execute',
            data=json.dumps({'agent_id': self.agent.id, 'workflow': workflow}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data['nodes']), 1)
