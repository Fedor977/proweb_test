from .models import Task, Comment
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


# Получение задач для пользователя
def get_tasks_for_user(user):
    """Получение списка задач для авторизованного пользователя"""
    return Task.objects.filter(user=user)


# Поиск задачи по id и пользователю
def get_task_by_id(user, task_id):
    """Получение задачи по id и пользователю"""
    return get_object_or_404(Task, id=task_id, user=user)


# Создание задачи
def create_task(user, task_data):
    """Создание новой задачи"""
    return Task.objects.create(user=user, **task_data)


# Обновление задачи
def update_task(user, task_id, task_data):
    """Обновление задачи по id"""
    task = get_task_by_id(user, task_id)
    if task.user != user:
        raise PermissionDenied("Вы не автор этой задачи.")
    for attr, value in task_data.items():
        setattr(task, attr, value)
    task.save()
    return task


# Удаление задачи
def delete_task(user, task_id):
    """Удаление задачи по id"""
    task = get_task_by_id(user, task_id)
    if task.user != user:
        raise PermissionDenied("Вы не автор этой задачи.")
    task.delete()


# Получение комментариев для задачи
def get_comments_for_task(task):
    """Получение комментариев к задаче"""
    return Comment.objects.filter(task=task).select_related('task')


# Создание комментария
def create_comment(user, task, comment_data):
    """Создание нового комментария к задаче"""
    if 'task' in comment_data:
        del comment_data['task']

    return Comment.objects.create(user=user, task=task, **comment_data)
