from django.test import TestCase
from .models import Task, Event


class TaskModelTest(TestCase):
    def test_task_model_exists(self):
        task_count = Task.objects.count()

        self.assertEqual(task_count, 0)

    def test_model_has_string_representation(self):
        task = Task.objects.create(
            title="First task", date="0001-01-01", task_id="test000000"
        )

        self.assertEqual(str(task), task.title)


class EventModelTest(TestCase):
    def test_event_model_exists(self):
        event_count = Event.objects.count()

        self.assertEqual(event_count, 0)

    def test_model_has_string_representation(self):
        event = Event.objects.create(
            summary="First event", date="0001-01-01", event_id="test000000"
        )

        self.assertEqual(str(event), event.summary)


class ApiGetEndpointsTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="First task", date="0001-01-01", task_id="test000000"
        )

        self.event = Event.objects.create(
            summary="First event", date="0001-01-01", event_id="test000000"
        )

    def test_root_get_endpoint_for_tasks_returns_correct_response(self):
        response = self.client.get("/api/v1/tasks/")

        self.assertEqual(response.status_code, 200)

    def test_root_get_endpoint_for_events_returns_correct_response(self):
        response = self.client.get("/api/v1/events/")

        self.assertEqual(response.status_code, 200)

    def test_date_range_endpoint_for_tasks_returns_correct_response(self):
        response = self.client.get("/api/v1/tasks/2024-01-01/2024-01-02/")

        self.assertEqual(response.status_code, 200)

    def test_date_range_endpoint_for_events_returns_correct_response(self):
        response = self.client.get("/api/v1/events/2024-01-01/2024-01-02/")

        self.assertEqual(response.status_code, 200)

    def test_retrieve_endpoint_for_tasks_returns_correct_response(self):
        response = self.client.get(f"/api/v1/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, 200)

    def test_retrieve_endpoint_for_events_returns_correct_response(self):
        response = self.client.get(f"/api/v1/events/{self.event.id}/")

        self.assertEqual(response.status_code, 200)

    def test_retrieve_endpoint_for_tasks_contains_event(self):
        response = self.client.get(f"/api/v1/tasks/{self.task.id}/")

        self.assertContains(response, self.task.title)

    def test_retrieve_endpoint_for_events_contains_event(self):
        response = self.client.get(f"/api/v1/events/{self.event.id}/")

        self.assertContains(response, self.event.summary)

    def test_root_get_endpoint_has_tasks(self):
        response = self.client.get("/api/v1/tasks/")

        self.assertContains(response, self.task)

    def test_root_get_endpoint_has_events(self):
        response = self.client.get("/api/v1/events/")

        self.assertContains(response, self.event)
