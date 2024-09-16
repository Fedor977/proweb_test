from rest_framework.test import APIClient
from django.test import TestCase

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_task_filter_by_status(self):
        response = self.client.get('/api/tasks/', {'status': 'Completed'})
        self.assertEqual(response.status_code, 200)
        for task in response.data['results']:
            self.assertEqual(task['status'], 'Completed')
