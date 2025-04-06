from django.db import models

# Create your models here.

class Category(models.Model):
 name = models.CharField(max_length=100)
 def __str__(self):
  return self.name

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

 def __str__(self):
  return self.title

 class Meta:
  constraints = [
   models.UniqueConstraint(fields=['title', 'created_date'], name='unique_title_per_day')
  ]



class SubTask(models.Model):
 title = models.CharField(max_length=100)
 description = models.TextField(null=True, blank=True)
 status = models.CharField(max_length=30,
                           choices=Task.STATUS_CHOICES)
 task = models.ForeignKey(Task, on_delete=models.CASCADE)
 deadline = models.DateTimeField()
 created_at = models.DateTimeField(auto_now_add=True)
 def __str__(self):
  return self.title
