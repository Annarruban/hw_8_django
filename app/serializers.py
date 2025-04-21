from app.models import Task, SubTask, Category
from django.utils import timezone
from rest_framework import serializers



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
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'deadline'
        ]


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


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'deadline',
            'subtasks'
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    def _assert_name_unique(self, name):
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Already exists")

    def create(self, validated_data):
        self._assert_name_unique(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._assert_name_unique(validated_data['name'])
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        fields = [
            'name'
        ]