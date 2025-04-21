from app.models import Task, SubTask, Category

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