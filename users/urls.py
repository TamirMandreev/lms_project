from rest_framework.routers import SimpleRouter

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

]

urlpatterns += router_payment.urls
urlpatterns += router_user.urls