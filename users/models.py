from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

from materials.models import Course, Lesson

# Create your models here.


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи "

    def __str__(self):
        return self.email


# Создать класс Платеж
class Payment(models.Model):

    CACH = 1  # Наличный способ оплаты
    BANK_TRANSFER = 2  # Безналичный способ оплаты

    STATUS_CHOICES = [(CACH, "Наличные"), (BANK_TRANSFER, "Банковский перевод")]

    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="payments",
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    # Дата оплаты
    # auto_now_add используется для автоматического заполнения поля значением
    # текущей даты и времени при создании записи
    payment_date = models.DateTimeField(auto_now_add=True)
    # Оплаченный курс или урок
    paid_course = models.ForeignKey(
        Course,
        on_delete=CASCADE,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=CASCADE,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    # Метод оплаты
    payment_method = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )

    # Сумма платежа
    amount = models.PositiveIntegerField(
        verbose_name="Сумма платежа", help_text="Укажите сумму платежа"
    )
    # Id сессии
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
    )
    # Ссылка на оплату
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.amount
