from django.contrib import admin

from app.models import Task, SubTask, Category  # импорт нужных моделей из нужного приложения

# в этом файле мы регистрируем те модели, которые нужны нам в работе в Админ панели по URL /admin


admin.site.register(Task)  # Регистрация модели Task
admin.site.register(SubTask)  # Регистрация модели SubTask
admin.site.register(Category)  # Регистрация модели профиля Category
