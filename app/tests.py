from django.test import TestCase
from django.utils import timezone
import time
from .models import Task, TaskSample


class AutoLabelTests(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            user_id=1,
            username='tester',
            sort=0,
            code='task1',
            name='task1',
            task_type=1,
            remark='',
            sample_annotation_count=0,
            sample_count=1,
            labels='[]',
            create_time=timezone.now(),
            create_timestamp=int(time.time()),
            last_update_time=timezone.now(),
            state=1,
        )
        TaskSample.objects.create(
            sort=0,
            code='sample1',
            user_id=1,
            username='tester',
            task_type=1,
            task_code='task1',
            old_filename='a.jpg',
            new_filename='a.jpg',
            remark='',
            create_time=timezone.now(),
            state=1,
            annotation_user_id=0,
            annotation_username='',
            annotation_time=timezone.now(),
            annotation_content='',
            annotation_state=0,
            annotation_model='',
            annotation_params='',
        )

    def test_auto_label_flow(self):
        response = self.client.post(
            '/api/auto_label/start',
            data={'task_code': 'task1', 'sample_codes': ['sample1']},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        job_id = response.json()['data']['job_id']

        response = self.client.get('/api/auto_label/progress', {'job_id': job_id})
        self.assertEqual(response.status_code, 200)
        progress = response.json()['data']
        self.assertEqual(progress['total'], 1)
        self.assertEqual(progress['finished'], 1)

        sample = TaskSample.objects.get(code='sample1')
        self.assertEqual(sample.annotation_state, 1)
        self.assertEqual(sample.annotation_model, 'image-model')
