from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User


@shared_task
def block_inactive_users():
    """Если last_login пользователя позже 30 дней назад, поле is_active=False"""
    # Вычислить дату 30 дней назад
    one_month_ago = now() - timedelta(days=30)
    # Получить всех пользователей, чей last_login позже 30 дней назад
    inactive_users = User.objects.filter(is_active=True, last_login__lt=one_month_ago)
    # Заблокировать их
    inactive_users.update(is_active=False)

    return f"{len(inactive_users)} пользователей заблокировано"
