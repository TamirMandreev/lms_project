from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscribe
from users.models import User


# Create your tests here.

class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.course = Course.objects.create(name='Test Course', description='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Lesson', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            'name': 'Test Lesson',
            'description': 'Test Lesson',
            'course': self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_to_video": None,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_detail(self):
        url = reverse('materials:lesson-detail', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=[self.lesson.pk])
        data = {
            'name': 'Test Lesson 2',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data.get('name'), 'Test Lesson 2')

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.course = Course.objects.create(name='Test Course', description='Test Course', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_true(self):
        url = reverse('materials:subscribe')
        data = {'course_id': self.course.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Сообщение'], 'Подписка добавлена')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['Сообщение'], 'Подписка удалена')







