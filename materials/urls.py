from django.urls import path

# SimpleRouter автоматически создает маршруты для стандартных
# CRUD операций (GET, POST, PATCH, DELETE),
# основываясь на представлении, переданном ему
from rest_framework.routers import SimpleRouter

from materials import views
from materials.apps import MaterialsConfig
from materials.views import CourseViewSet

app_name = MaterialsConfig.name

# Создать экземпляр роутера
router = SimpleRouter()
router.register("courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", views.LessonListAPIView.as_view(), name="lesson-list"),
    path(
        "lessons/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-detail"
    ),
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
    path(
        "lessons/update/<int:pk>/",
        views.LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "lessons/delete/<int:pk>/",
        views.LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
    path("subscribe/", views.SubscribeAPIView.as_view(), name="subscribe"),
]

urlpatterns += router.urls
