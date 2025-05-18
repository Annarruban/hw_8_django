from django.db.models import Count
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app.models.category import Category
from app.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]


    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = Category.objects.annotate(task_count=Count('tasks'))
        data = {category.name: category.task_count for category in categories}
        return Response(data)