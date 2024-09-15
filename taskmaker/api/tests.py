from django.test import TestCase
from .models import Task, Event
import json


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


class GetEndpointsReturnsCorrectResponseTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="First task", date="2024-01-01", task_id="test000000"
        )

        self.event = Event.objects.create(
            summary="First event", date="2024-01-01", event_id="test000000"
        )

    def test_root_endpoint_for_tasks_returns_correct_response(self):
        response = self.client.get("/api/v1/tasks/")

        self.assertEqual(response.status_code, 200)

    def test_root_endpoint_for_events_returns_correct_response(self):
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


class RequestsHasCorrectContentTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="First task", date="2024-01-01", task_id="test000000"
        )

        self.task_foo = Task.objects.create(
            title="Second task", date="2024-01-10", task_id="test000000"
        )

        self.event = Event.objects.create(
            summary="First event", date="2024-01-01", event_id="test000000"
        )

        self.event_foo = Event.objects.create(
            summary="Second event", date="2024-01-10", event_id="test000000"
        )

    def test_root_endpoint_has_task(self):
        response = self.client.get("/api/v1/tasks/")

        self.assertTaskContent(response)

    def test_root_endpoint_has_event(self):
        response = self.client.get("/api/v1/events/")

        self.assertEventContent(response)

    def test_root_endpoint_search_query_has_task(self):
        response = self.client.get("/api/v1/tasks/?search=rst")

        self.assertContains(response, self.task.title)

    def test_root_endpoint_search_query_has_event(self):
        response = self.client.get("/api/v1/events/?search=rst")

        self.assertContains(response, self.event.summary)

    def test_retrieve_endpoint_for_tasks_has_task(self):
        response = self.client.get(f"/api/v1/tasks/{self.task.id}/")

        self.assertTaskContent(response)
        self.assertNotContains(response, self.task_foo)

    def test_retrieve_endpoint_for_events_has_event(self):
        response = self.client.get(f"/api/v1/events/{self.event.id}/")

        self.assertEventContent(response)
        self.assertNotContains(response, self.event_foo)

    def test_date_range_endpoint_for_tasks_has_correct_task(self):
        response = self.client.get("/api/v1/tasks/2024-01-01/2024-01-02/")

        self.assertTaskContent(response)
        self.assertNotContains(response, self.task_foo)

    def test_date_range_endpoint_for_events_has_correct_event(self):
        response = self.client.get("/api/v1/events/2024-01-01/2024-01-02/")

        self.assertEventContent(response)
        self.assertNotContains(response, self.event_foo)

    def test_post_method_for_tasks(self):
        task_post_test = {"title": "Post test", "date": "2024-01-01"}
        response = self.client.post(
            "/api/v1/tasks/",
            json.dumps(task_post_test),
            content_type="application/json",
        )

        self.assertContains(response, task_post_test["title"], status_code=201)
        self.assertContains(response, task_post_test["date"], status_code=201)
        self.assertEqual(Task.objects.count(), 3)

    def test_post_method_for_events(self):
        event_post_test = {"summary": "Post test", "date": "2024-01-01"}
        response = self.client.post(
            "/api/v1/events/",
            json.dumps(event_post_test),
            content_type="application/json",
        )

        self.assertContains(response, event_post_test["summary"], status_code=201)
        self.assertContains(response, event_post_test["date"], status_code=201)
        self.assertEqual(Event.objects.count(), 3)

    def test_put_method_for_tasks(self):
        task_put_test = {"title": "Put test", "date": "2024-02-02"}
        response = self.client.put(
            f"/api/v1/tasks/{self.task.id}/",
            json.dumps(task_put_test),
            content_type="application/json",
        )

        self.assertContains(response, task_put_test["title"])
        self.assertContains(response, task_put_test["date"])

        response = self.client.get(f"/api/v1/tasks/{self.task.id}/")

        self.assertContains(response, task_put_test["title"])
        self.assertContains(response, task_put_test["date"])

    def test_put_method_for_events(self):
        event_put_test = {"summary": "Put test", "date": "2024-02-02"}
        response = self.client.put(
            f"/api/v1/events/{self.event.id}/",
            json.dumps(event_put_test),
            content_type="application/json",
        )

        self.assertContains(response, event_put_test["summary"])
        self.assertContains(response, event_put_test["date"])

        response = self.client.get(f"/api/v1/events/{self.event.id}/")

        self.assertContains(response, event_put_test["summary"])
        self.assertContains(response, event_put_test["date"])

    def test_delete_method_for_tasks(self):
        self.assertEqual(Task.objects.count(), 2)

        response = self.client.delete(f"/api/v1/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_method_for_events(self):
        self.assertEqual(Event.objects.count(), 2)

        response = self.client.delete(f"/api/v1/events/{self.event.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Event.objects.count(), 1)

    def assertTaskContent(self, response):
        self.assertContains(response, self.task)
        self.assertContains(response, self.task.date)
        self.assertContains(response, self.task.task_id)

    def assertEventContent(self, response):
        self.assertContains(response, self.event)
        self.assertContains(response, self.event.date)
        self.assertContains(response, self.event.event_id)
