from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name =  UsersConfig.name

# Создать экземпляр роутера. Роутер отвечает за автоматическое
# создание маршрутов для ViewSet на основе стандартных действий CRUD
router = SimpleRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [

]

urlpatterns += router.urls