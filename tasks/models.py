from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:position-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="assigned_tasks",
        blank=True,
    )

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})
