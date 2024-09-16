from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TaskSerializer, CommentSerializer
from .services import get_tasks_for_user, get_task_by_id, get_comments_for_task, create_comment, delete_task
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Task


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES, label='Status')  # Добавьте это для фильтрации по статусу

    class Meta:
        model = Task
        fields = ['status', 'due_date']


class TaskViewSet(viewsets.ModelViewSet):
    """Реализация функционала для работы с задачами через ModelViewSet"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    # добавляем фильтрацию, поиск, сортировку
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        """Получение списка задач для авторизованного пользователя через сервис"""
        return get_tasks_for_user(self.request.user)

    def retrieve(self, request, pk=None):
        """Получение информации конкретной задачи по id через сервис"""
        task = get_task_by_id(request.user, pk)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Создание новой задачи через сервис"""
        task_data = self.request.data
        task = serializer.save(user=self.request.user, **task_data)
        return task

    def perform_update(self, serializer):
        """Обновление задачи через сервис"""
        task_data = self.request.data
        task = serializer.save(user=self.request.user, **task_data)
        return task

    def perform_destroy(self, instance):
        """Удаление задачи через сервис"""
        delete_task(self.request.user, instance.id)


class CommentViewSet(viewsets.ModelViewSet):
    """Реализация функционала для работы с комментариями через ModelViewSet"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Получение комментариев к конкретной задаче через сервис"""
        task_pk = self.kwargs['task_pk']
        task = get_task_by_id(self.request.user, task_pk)
        return get_comments_for_task(task)

    def perform_create(self, serializer):
        """Создание нового комментария к задаче через сервис"""
        task_pk = self.kwargs['task_pk']
        task = get_task_by_id(self.request.user, task_pk)
        create_comment(self.request.user, task, self.request.data)
