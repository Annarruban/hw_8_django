from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import filters, generics

from app.models import Task
from app.serializers.task import TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method == 'POST' else TaskListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        day_of_week = self.request.query_params.get('day_of_week')
        if day_of_week:
            queryset = queryset.filter(created_at__week_day=day_of_week)
        return queryset


@api_view(['GET'])
def task_stats(request) -> Response:
    res = {
        "total": Task.objects.all().count(),
        "past_deadline": Task.objects.filter(
            deadline__lt=timezone.now()
        ).exclude(status="Done").count(),
        **{
            o["status"]: o["count"] for o in
            Task.objects.values('status').annotate(count=Count('id'))
        }
    }

    return Response(
        data=res,
        status=200
    )


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer