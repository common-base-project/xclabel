from django.views.decorators.csrf import csrf_exempt
from app.views.ViewsBase import parse_post_params, HttpResponseJson
from ..models import LLMProvider
from ..providers import get_provider


@csrf_exempt
def api_chat(request):
    if request.method != 'POST':
        return HttpResponseJson({'code': 0, 'msg': 'only POST allowed'})
    params = parse_post_params(request)
    provider_id = params.get('provider_id')
    model = params.get('model')
    messages = params.get('messages', [])
    try:
        provider = LLMProvider.objects.filter(id=provider_id, is_active=True).first()
        if not provider:
            raise Exception('provider not found')
        impl = get_provider(provider.type, base_url=provider.base_url, api_key=provider.api_key)
        data = impl.chat(messages=messages, model=model)
        return HttpResponseJson({'code': 1000, 'data': data})
    except Exception as e:
        return HttpResponseJson({'code': 0, 'msg': str(e)})


@csrf_exempt
def api_image(request):
    return HttpResponseJson({'code': 0, 'msg': 'not implemented'})


@csrf_exempt
def api_video(request):
    return HttpResponseJson({'code': 0, 'msg': 'not implemented'})


@csrf_exempt
def api_analyze(request):
    return HttpResponseJson({'code': 0, 'msg': 'not implemented'})
