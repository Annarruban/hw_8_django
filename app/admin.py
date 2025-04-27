from django.contrib import admin
from django.db.models import QuerySet

from app.models import Task, SubTask
from app.models.category import Category


# в этом файле мы регистрируем те модели, которые нужны нам в работе в Админ панели по URL /admin

class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]

    list_display = ('short_task', 'status', 'created_at', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'created_date')

    def short_task(self, obj: Task) -> str:
        return f"{obj.title[:10]}..."

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

    actions = ['update_status_to_done']

    def update_status_to_done(self, request, objects: QuerySet) -> None:
        for obj in objects:
            obj.status = "Done"

            obj.save()

    update_status_to_done.short_description = "Обновить статус -> Done"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)