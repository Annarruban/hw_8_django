from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')  # уникальность по полю name
        ]


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


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30,
                              choices=Task.STATUS_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Meta:
    db_table = 'task_manager_subtask'
    ordering = ['-created_at']
    verbose_name = 'SubTask'
    constraints = [
        models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
    ]
