from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscribe
from materials.paginators import CustomPaginator
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from materials.tasks import send_information_about_update_course
from users.permissions import IsModerator, IsOwner


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        '''
        Сохраняет изменения в объекте и отправляет уведомления подписчикам о произошедшем обновлении.
        '''
        # Сохраняем объект с новыми данными
        serializer.save()
        # Получить pk обновляемого объекта
        updated_course = serializer.instance
        # Получить подписки, связанные с обновляемым курсом
        subscribes = updated_course.subscribed_courses.all()
        # Создать переменную для хранения email-адресов пользователей, у которых есть подписка на курс
        email_list = []
        # Добавить email-адреса
        for subscribe in subscribes:
            if subscribe.user.email:
                email = subscribe.user.email
                email_list.append(email)
        # Отправить уведомления об обновлении курса на все email-адреса
        send_information_about_update_course(email_list, updated_course.name)







# Представления на основе Generics
class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CustomPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscribeAPIView(APIView):
    serializer_class = SubscribeSerializer

    def post(self, request):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = Course.objects.get(id=course_id)

        subscribe_item = Subscribe.objects.filter(user=user, course=course_item)

        if subscribe_item.exists():
            subscribe_item.delete()
            message = 'Подписка удалена'
        else:
            Subscribe.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({'Сообщение': message})



