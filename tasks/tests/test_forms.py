from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.forms import (
    PositionNameSearchForm,
    TaskForm,
    TaskNameSearchForm,
    TaskTypeNameSearchForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    WorkerPositionUpdateForm,
    WorkerUsernameSearchForm,
    LoginForm,
)
from tasks.models import Position, TaskType


class FormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="DevOps")
        self.task_type = TaskType.objects.create(name="Feature")
        self.worker = get_user_model().objects.create_user(
            username="devops_user",
            password="password123",
        )

    def test_task_form_valid_data(self):
        form_data = {
            "name": "Deploy app",
            "description": "Deploy to production",
            "deadline": "2026-10-15",
            "priority": "urgent",
            "task_type": self.task_type.pk,
            "assignees": [self.worker.pk],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_assignees_excludes_superuser(self):
        admin = get_user_model().objects.create_superuser(
            username="admin_user",
            email="admin@test.com",
            password="adminpassword123",
        )
        form = TaskForm()
        assignees_qs = form.fields["assignees"].queryset
        self.assertIn(self.worker, assignees_qs)
        self.assertNotIn(admin, assignees_qs)

    def test_worker_creation_form(self):
        form_data = {
            "username": "newworker",
            "email": "newworker@company.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "position": self.position.pk,
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_update_form(self):
        form_data = {
            "username": "updated_username",
            "email": "updated@company.com",
            "first_name": "Bob",
            "last_name": "Brown",
            "position": self.position.pk,
        }
        form = WorkerUpdateForm(instance=self.worker, data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        form = LoginForm(
            data={"username": "devops_user", "password": "password123"}
        )
        self.assertTrue(form.is_valid())

    def test_worker_position_update_form(self):
        form = WorkerPositionUpdateForm(
            data={"position": self.position.pk}
        )
        self.assertTrue(form.is_valid())

    def test_search_forms(self):
        task_search = TaskNameSearchForm(data={"name": "test"})
        self.assertTrue(task_search.is_valid())
        worker_search = WorkerUsernameSearchForm(data={"username": "test"})
        self.assertTrue(worker_search.is_valid())
        pos_search = PositionNameSearchForm(data={"name": "test"})
        self.assertTrue(pos_search.is_valid())
        type_search = TaskTypeNameSearchForm(data={"name": "test"})
        self.assertTrue(type_search.is_valid())
