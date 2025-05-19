from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    def __str__(self):
        return self.title

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='task_manager_task')
        ]

    db_table = 'task_manager_task'
    ordering = ['-created_at']
    verbose_name = 'Task'
