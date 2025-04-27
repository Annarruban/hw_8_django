from app.models import Task, SubTask
from rest_framework import serializers


class SubTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    task_id = serializers.IntegerField()

    deadline = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'task_id',
            'created_at'
        ]


class SubTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'status',
            'deadline',
            'task_id'
        ]
