from django.contrib import admin
from app.models import Task, SubTask, Category

# в этом файле мы регистрируем те модели, которые нужны нам в работе в Админ панели по URL /admin

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'created_date')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)