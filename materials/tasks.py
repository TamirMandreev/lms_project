from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course


# Декоратор shared_task используется для обозначения функции как задачи,
# доступной для выполнения в асинхронном режиме
@shared_task
def send_information_about_update_course(pk):
    # Получить обновляемый курс
    updated_course = Course.objects.get(pk=pk)
    # Получить подписки, связанные с обновляемым курсом
    subscriptions = updated_course.subscribed_courses.all()
    # Непонятное действие
    email_list = list(subscriptions.values_list("user__email", flat=True))
    """Отправляет сообщение пользователям об обновлении курса"""
    send_mail(
        f"Обновление курса {updated_course.name}",
        f"Курс {updated_course.name} обновился",
        EMAIL_HOST_USER,
        email_list,
    )
