from django.urls import path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

app_name =  UsersConfig.name

# Создать экземпляр роутера. Роутер отвечает за автоматическое
# создание маршрутов для ViewSet на основе стандартных действий CRUD
router_payment = SimpleRouter()
router_user = SimpleRouter()

router_payment.register('payments', PaymentViewSet, basename='payments')
router_user.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

urlpatterns += router_payment.urls
urlpatterns += router_user.urls