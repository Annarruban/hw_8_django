import os
import django
from django.utils import timezone

(os.environ.setdefault
 ('DJANGO_SETTINGS_MODULE', 'my_project.settings'))
django.setup()

from app.models.subtask import SubTask
from app.models.task import Task
from app.models.category import Category
import datetime
from django.db.models import F

# Выполните запросы:
# Создание записей:
#
# Task:
# title: "Prepare presentation".
# description: "Prepare materials and slides for the presentation".
# status: "New".
# deadline: Today's date + 3 days.

"""
deadline_date = datetime.datetime.now() + datetime.timedelta(days=3)

Task.objects.create(title='Prepare presentation',
                    description='Prepare meterials and slides for the presentation',
                    status='New',
                    deadline=deadline_date
                    )

"""


# SubTasks для "Prepare presentation":
# title: "Gather information".
# description: "Find necessary information for the presentation".
# status: "New".
# deadline: Today's date + 2 days.
task_obj = Task.objects.get(title='Prepare presentation')
"""
deadline_date2 = datetime.datetime.now() + datetime.timedelta(days=2)


SubTask.objects.create(title='Gather information',
                       description='Find necessary information for the presentation',
                       status='New',
                       deadline=deadline_date2,
                       task=task_obj
                    )
"""
# title: "Create slides".
# description: "Create presentation slides".
# status: "New".
# deadline: Today's date + 1 day.#
"""
deadline_date3 = datetime.datetime.now() + datetime.timedelta(days=1)

SubTask.objects.create(title='Create slides',
                       description='Create presentation slide',
                       status='New',
                       deadline=deadline_date3,
                       task=task_obj
                    )
"""
# Чтение записей:
# Tasks со статусом "New":
# Вывести все задачи, у которых статус "New".

tasks = Task.objects.filter(status='New')

for t in tasks:
 print(t)

# SubTasks с просроченным статусом "Done":
# Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.

deadline_today = timezone.make_aware(datetime.datetime.now())

subtasks = SubTask.objects.filter(status='Done', deadline__lt=deadline_today).values()

for s in subtasks:
    print(s)

# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".

Task.objects.filter(title="Prepare presentation").update(status="In progress")
updated_task = Task.objects.filter(title="Prepare presentation")
print(updated_task.values())

# Измените срок выполнения для "Gather information" на два дня назад.

SubTask.objects.filter(title="Gather information").update(deadline=F('deadline') - datetime.timedelta(days=2))
s_task = SubTask.objects.filter(title="Gather information")
print(s_task.values())

# Измените описание для "Create slides" на "Create and format presentation slides".

SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")
s_task2 = SubTask.objects.filter(title="Create slides")
print(s_task2.values())


# Удаление записей:
#
# Удалите задачу "Prepare presentation" и все ее подзадачи.

Task.objects.filter(title="Prepare presentation").delete()