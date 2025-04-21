from app.models import Task, SubTask

from rest_framework import serializers


class TaskCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    deadline = serializers.DateTimeField()

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'deadline'
        ]

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'deadline'
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)

    deadline = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'created_at'
        ]