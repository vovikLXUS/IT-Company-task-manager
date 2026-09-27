from django.contrib import admin
from django.test import TestCase

from tasks.models import Position, Task, TaskType, Worker


class AdminTests(TestCase):
    def test_models_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Position))
        self.assertTrue(admin.site.is_registered(TaskType))
        self.assertTrue(admin.site.is_registered(Task))
        self.assertTrue(admin.site.is_registered(Worker))
