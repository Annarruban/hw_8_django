from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Task, SubTask
from app.serializers import TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer, SubTaskSerializer, \
    SubTaskListSerializer


def user_greetings(request):
    name = "Anna"
    return HttpResponse(
        f"<h2>Hello, {name}!</h2>")


@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_of_tasks(request) -> Response:
    filters = {}
    day_of_week = request.query_params.get('day_of_week')

    if day_of_week:
        filters['created_at__week_day'] = day_of_week

    tasks = Task.objects.filter(**filters)

    serializer = TaskListSerializer(tasks, many=True)

    return Response(
        data=serializer.data,
        status=200
    )

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

@api_view(['GET'])
def get_task_detail(request, task_id: int) -> Response:
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            data={
                "message": "TASK NOT FOUND"
            },
            status=404
        )

    serializer = TaskDetailSerializer(task)

    return Response(
        data=serializer.data,
        status=200
    )


class SubtaskListCreateView(APIView, PageNumberPagination):
    DEFAULT_PAGE_SIZE = 5

    def get(self, request):
        page_size = request.query_params.get('page_size')
        self.page_size = page_size if page_size and page_size.isdigit() else self.DEFAULT_PAGE_SIZE

        subtasks = self.paginate_queryset(
            SubTask.objects.all().order_by('-created_at'), request, view=self
        )

        serializer = SubTaskListSerializer(subtasks, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(
                {'error': 'Subtask not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'},
                status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskSerializer(subtask, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'},
                status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)