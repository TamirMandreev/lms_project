from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'