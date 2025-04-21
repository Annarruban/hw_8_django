"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_project import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from app.views import task_create, list_of_tasks, get_task_detail, task_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greetings/', views.user_greetings),
    path('task/create/', task_create),
    path('task/', list_of_tasks),
    path('task/<int:task_id>/', get_task_detail),
    path('task/stats/', task_stats),
]
