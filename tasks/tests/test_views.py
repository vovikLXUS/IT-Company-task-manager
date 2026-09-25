from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Position, Task, TaskType


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="QA Engineer")
        self.task_type = TaskType.objects.create(name="QA")
        self.user = get_user_model().objects.create_user(
            username="logged_in_user",
            password="securepassword123",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="Verify releases",
            description="Check release build",
            deadline=date(2026, 11, 1),
            priority=Task.PriorityChoices.MEDIUM,
            task_type=self.task_type,
        )

    def test_index_view_login_required(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_index_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)
        self.assertEqual(response.context["num_positions"], 1)
        self.assertEqual(response.context["num_task_types"], 1)

    def test_task_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Verify releases")

    def test_task_list_search(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("tasks:task-list"), {"name": "Verify"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)

        response = self.client.get(
            reverse("tasks:task-list"), {"name": "NonExisting"}
        )
        self.assertEqual(len(response.context["task_list"]), 0)

    def test_task_detail_view(self):
        self.client.force_login(self.user)
        url = reverse("tasks:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        self.client.force_login(self.user)
        url = reverse("tasks:task-create")
        data = {
            "name": "New Task",
            "description": "Details",
            "deadline": "2026-12-01",
            "priority": "low",
            "task_type": self.task_type.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_worker_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class ToggleAssignToTaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task_type = TaskType.objects.create(name="Feature")
        self.user = get_user_model().objects.create_user(
            username="worker_assignee",
            password="secretpassword",
        )
        self.task = Task.objects.create(
            name="Implement Feature X",
            description="Feature details",
            deadline=date(2026, 10, 10),
            priority=Task.PriorityChoices.MEDIUM,
            task_type=self.task_type,
        )

    def test_toggle_assign_login_required(self):
        url = reverse(
            "tasks:toggle-task-assign", kwargs={"pk": self.task.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_toggle_assign_post_assigns_and_removes(self):
        self.client.force_login(self.user)
        url = reverse(
            "tasks:toggle-task-assign", kwargs={"pk": self.task.pk}
        )

        # 1. POST when not assigned -> assigns user
        self.assertNotIn(self.user, self.task.assignees.all())
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.task.assignees.all())

        # 2. POST when already assigned -> removes user
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.task.assignees.all())

    def test_toggle_assign_get_does_not_mutate_db(self):
        self.client.force_login(self.user)
        url = reverse(
            "tasks:toggle-task-assign", kwargs={"pk": self.task.pk}
        )

        # GET request should redirect without modifying assignees
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.task.assignees.all())

    def test_toggle_assign_non_existing_task_returns_404(self):
        self.client.force_login(self.user)
        url = reverse("tasks:toggle-task-assign", kwargs={"pk": 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
