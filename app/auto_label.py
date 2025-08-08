import json
import uuid
from django.utils import timezone
from .models import TaskSample

try:
    from django_q.tasks import async_task
except Exception:  # pragma: no cover - fallback when django-q is unavailable
    def async_task(func, *args, **kwargs):
        return func(*args, **kwargs)

# simple in-memory progress store
AUTO_LABEL_PROGRESS = {}


def choose_model(task_type):
    mapping = {
        1: 'image-model',
        2: 'video-model',
        3: 'audio-model',
    }
    return mapping.get(task_type, 'default-model')


def run_auto_label(job_id, task_code, sample_codes, model=None, params=None):
    total = len(sample_codes)
    AUTO_LABEL_PROGRESS[job_id] = {'total': total, 'finished': 0}
    for code in sample_codes:
        sample = TaskSample.objects.filter(task_code=task_code, code=code).first()
        if not sample:
            continue
        used_model = model or choose_model(sample.task_type)
        used_params = params or {}
        sample.annotation_user_id = 0
        sample.annotation_username = 'auto'
        sample.annotation_time = timezone.now()
        sample.annotation_content = f'auto labeled by {used_model}'
        sample.annotation_state = 1
        sample.annotation_model = used_model
        sample.annotation_params = json.dumps(used_params)
        sample.save()
        prog = AUTO_LABEL_PROGRESS[job_id]
        prog['finished'] += 1
    return True


def start_auto_label(task_code, sample_codes, model=None, params=None):
    job_id = str(uuid.uuid4())
    async_task(run_auto_label, job_id, task_code, sample_codes, model, params)
    return job_id


def get_progress(job_id):
    prog = AUTO_LABEL_PROGRESS.get(job_id, {'total': 0, 'finished': 0})
    total = prog.get('total', 0)
    finished = prog.get('finished', 0)
    percent = 0 if total == 0 else finished / total
    return {'total': total, 'finished': finished, 'percent': percent}

