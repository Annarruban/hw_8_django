from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')  # уникальность по полю name
        ]
