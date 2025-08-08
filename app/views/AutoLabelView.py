from app.views.ViewsBase import *
from app.auto_label import start_auto_label, get_progress


def api_start(request):
    ret = False
    msg = "未知错误"
    data = {}
    if request.method == 'POST':
        params = parse_post_params(request)
        task_code = params.get('task_code', '').strip()
        sample_codes = params.get('sample_codes', [])
        model = params.get('model', None)
        model_params = params.get('model_params', {})
        if isinstance(sample_codes, str):
            sample_codes = [s for s in sample_codes.split(',') if s]
        job_id = start_auto_label(task_code, sample_codes, model, model_params)
        ret = True
        msg = "success"
        data = {"job_id": job_id}
    res = {
        "code": 1000 if ret else 0,
        "msg": msg,
        "data": data,
    }
    return HttpResponseJson(res)


def api_progress(request):
    params = parse_get_params(request)
    job_id = params.get('job_id', '').strip()
    progress = get_progress(job_id)
    res = {
        "code": 1000,
        "msg": "success",
        "data": progress,
    }
    return HttpResponseJson(res)

