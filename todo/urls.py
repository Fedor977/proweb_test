from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/tasks/<int:task_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-comments-list-create'),
    path('api/tasks/<int:task_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-comments-detail'),
]
