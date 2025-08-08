import json
from uuid import uuid4

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from llm.providers import get_provider
from .models import Agent, AgentSession, WorkflowSession


@csrf_exempt
def chat(request):
    """Handle chat requests for a given agent."""

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body.decode("utf-8") or "{}")
    agent_id = data.get("agent_id")
    prompt = data.get("message", "")
    session_id = data.get("session_id") or uuid4().hex

    agent = get_object_or_404(Agent, pk=agent_id)
    provider_impl = get_provider(
        agent.provider.type,
        api_key=agent.provider.api_key,
        base_url=agent.provider.base_url,
    )

    session, _ = AgentSession.objects.get_or_create(agent=agent, session_id=session_id)
    messages = session.messages
    messages.append({"role": "user", "content": prompt})
    result = provider_impl.chat(messages, model=agent.config.get("model"))
    reply = result.get("reply") if isinstance(result, dict) else result
    messages.append({"role": "assistant", "content": reply})
    session.messages = messages
    session.save()

    return JsonResponse({
        "session_id": session.session_id,
        "reply": reply,
        "messages": messages,
    })


@csrf_exempt
def execute_workflow(request):
    """Execute a simple sequential workflow for an agent."""

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body.decode("utf-8") or "{}")
    agent_id = data.get("agent_id")
    workflow_nodes = data.get("workflow", [])
    session_id = data.get("session_id") or uuid4().hex

    agent = get_object_or_404(Agent, pk=agent_id)
    provider_impl = get_provider(
        agent.provider.type,
        api_key=agent.provider.api_key,
        base_url=agent.provider.base_url,
    )

    session, _ = WorkflowSession.objects.get_or_create(agent=agent, session_id=session_id)
    executed_nodes = session.nodes

    for node in workflow_nodes:
        prompt = node.get("prompt", "")
        result = provider_impl.chat([{ "role": "user", "content": prompt }], model=agent.config.get("model"))
        reply = result.get("reply") if isinstance(result, dict) else result
        executed_nodes.append({
            "id": node.get("id"),
            "prompt": prompt,
            "reply": reply,
        })

    session.nodes = executed_nodes
    session.save()

    return JsonResponse({
        "session_id": session.session_id,
        "nodes": executed_nodes,
    })
