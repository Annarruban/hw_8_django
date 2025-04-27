from app.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
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