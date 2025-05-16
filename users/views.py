from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from materials.models import Course
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    create_strip_price,
    create_strip_product,
    create_strip_session,
)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    ordering_fields = ("payment_date",)
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )

    # Переопределить создание объекта модели
    def perform_create(self, serializer):
        # Создать объект платежа и связать его с текущим пользователем
        payment = serializer.save(user=self.request.user)
        # Получить оплачиваемый курс
        course_id = self.request.data.get("course_id")
        course = Course.objects.get(id=course_id)
        # Создать продукт
        product = create_strip_product(
            product_name=course.name, product_description=course.description
        )
        # Создать цену
        price = create_strip_price(payment.amount, product=product.id)
        # Создать сессию оплаты и получаем ссылку
        session_id, payment_link = create_strip_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
