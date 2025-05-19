from django.db import models
from django.contrib.auth.models import User


from app.models import Task


class SubTask(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30,
                              choices=Task.STATUS_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
