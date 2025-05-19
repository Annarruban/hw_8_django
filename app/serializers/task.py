from app.models import Task
from django.utils import timezone
from rest_framework import serializers

from app.serializers.subtask import SubTaskSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    deadline = serializers.DateTimeField()

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past")
        return value


    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'deadline'
        ]

class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'owner',
            'id',
            'title',
            'status',
            'deadline'
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    subtasks = SubTaskSerializer(many=True, read_only=True)
    read_only_fields = ['owner']

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'deadline',
            'subtasks',
            'owner'
        ]
