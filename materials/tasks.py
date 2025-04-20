from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from config.settings import EMAIL_HOST_USER
from users.models import User


# Декоратор shared_task используется для обозначения функции как задачи,
# доступной для выполнения в асинхронном режиме
@shared_task
def send_information_about_update_course(email_list, course_name):
    """Отправляет сообщение пользователям об обновлении курса"""
    send_mail(
        f"Обновление курса {course_name}",
        f"Курс {course_name} обновился",
        EMAIL_HOST_USER,
        email_list,
    )
