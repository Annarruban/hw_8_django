from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from app.models import Task
from app.serializers import TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer


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
    tasks = Task.objects.all()

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

