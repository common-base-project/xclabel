import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from ..models import LLMProvider


@csrf_exempt
def list_providers(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    providers = list(LLMProvider.objects.values())
    return JsonResponse({"providers": providers})


@csrf_exempt
def create_provider(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = json.loads(request.body.decode("utf-8") or "{}")
    provider = LLMProvider.objects.create(
        name=data.get("name", ""),
        type=data.get("type", ""),
        base_url=data.get("base_url", ""),
        api_key=data.get("api_key", ""),
        is_active=data.get("is_active", True),
        extra=json.dumps(data.get("extra", {})) if isinstance(data.get("extra"), (dict, list)) else data.get("extra", ""),
    )
    return JsonResponse({
        "id": provider.id,
        "name": provider.name,
        "type": provider.type,
        "base_url": provider.base_url,
        "api_key": provider.api_key,
        "is_active": provider.is_active,
        "extra": provider.extra,
    })


@csrf_exempt
def update_provider(request, pk: int):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponseNotAllowed(["PUT", "PATCH"])
    provider = get_object_or_404(LLMProvider, pk=pk)
    data = json.loads(request.body.decode("utf-8") or "{}")
    for field in ["name", "type", "base_url", "api_key", "is_active", "extra"]:
        if field in data:
            value = data[field]
            if field == "extra" and isinstance(value, (dict, list)):
                value = json.dumps(value)
            setattr(provider, field, value)
    provider.save()
    return JsonResponse({
        "id": provider.id,
        "name": provider.name,
        "type": provider.type,
        "base_url": provider.base_url,
        "api_key": provider.api_key,
        "is_active": provider.is_active,
        "extra": provider.extra,
    })


@csrf_exempt
def delete_provider(request, pk: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    provider = get_object_or_404(LLMProvider, pk=pk)
    provider.delete()
    return JsonResponse({"status": "deleted"})
