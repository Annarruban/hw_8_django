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
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app import views
from app.views.category import CategoryViewSet
from app.views.task import TaskListCreateView, UserTaskListView, TaskRetrieveUpdateDestroyView, task_stats
from app.views.subtask import SubtaskRetrieveUpdateDestroyView, SubtaskListCreateView

router = DefaultRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('greetings/', views.other.user_greetings),
    path('task/create/', TaskListCreateView.as_view(), name='task_create'),
    path('task/',  TaskListCreateView.as_view()),
    path('task/my', UserTaskListView.as_view()),
    path('task/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),
    path('task/stats/', task_stats),
    path('subtask/', SubtaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtask/<int:pk>/', SubtaskRetrieveUpdateDestroyView.as_view(),
         name='subtask-detail-update-delete'),
    path('', include(router.urls)),
]
