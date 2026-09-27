from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Position, Task, TaskType


class ModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = get_user_model().objects.create_user(
            username="testworker",
            password="testpassword123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="Fix critical bug",
            description="Fix login issue",
            deadline=date(2026, 12, 31),
            priority=Task.PriorityChoices.HIGH,
            task_type=self.task_type,
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "Developer")

    def test_position_get_absolute_url(self):
        expected_url = reverse(
            "tasks:position-detail", kwargs={"pk": self.position.pk}
        )
        self.assertEqual(self.position.get_absolute_url(), expected_url)

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username} (John Doe)",
        )

    def test_worker_get_absolute_url(self):
        expected_url = reverse(
            "tasks:worker-detail", kwargs={"pk": self.worker.pk}
        )
        self.assertEqual(self.worker.get_absolute_url(), expected_url)

    def test_worker_position_set_null_on_delete(self):
        self.assertEqual(self.worker.position, self.position)
        self.position.delete()
        self.worker.refresh_from_db()
        self.assertIsNone(self.worker.position)
        self.assertTrue(
            get_user_model().objects.filter(pk=self.worker.pk).exists()
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Fix critical bug")

    def test_task_get_absolute_url(self):
        expected_url = reverse(
            "tasks:task-detail", kwargs={"pk": self.task.pk}
        )
        self.assertEqual(self.task.get_absolute_url(), expected_url)

    def test_task_assignees_relationship(self):
        self.task.assignees.add(self.worker)
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertIn(self.task, self.worker.assigned_tasks.all())
