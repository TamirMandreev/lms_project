from django.urls import path
# SimpleRouter автоматически создает маршруты для стандартных
# CRUD операций (GET, POST, PATCH, DELETE),
# основываясь на представлении, переданном ему
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet

app_name = MaterialsConfig.name

# Создать экземпляр роутера
router = SimpleRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [

]

urlpatterns += router.urls