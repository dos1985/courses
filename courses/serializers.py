from rest_framework import serializers
from .models import Product, ProductAccess, Lesson, ProductLesson, LessonView


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'owner', 'created', 'updated']


class ProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = ['id', 'product', 'user', 'created', 'updated']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'duration', 'created', 'updated']


class ProductLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLesson
        fields = ['id', 'product', 'lesson', 'created', 'updated']


class LessonViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)  # Получаем отображаемое значение статуса

    class Meta:
        model = LessonView
        fields = ['id', 'lesson', 'user', 'view_duration', 'status', 'created', 'updated']
