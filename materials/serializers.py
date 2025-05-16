from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscribe
from materials.validators import url_validator


class LessonSerializer(ModelSerializer):
    link_to_video = serializers.CharField(validators=[url_validator], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """
        Возвращает True, если текущий пользователь подписан на курс, иначе False.
        """
        current_user = self.context["request"].user
        try:
            Subscribe.objects.get(user=current_user, course=course)
            return True
        except Subscribe.DoesNotExist:
            return False


class SubscribeSerializer(ModelSerializer):

    class Meta:
        model = Subscribe
        fields = "__all__"
