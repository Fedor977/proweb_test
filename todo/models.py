from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, verbose_name='Имя задачи')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name='Статус')
    due_date = models.DateField(blank=True, null=True, verbose_name='Срок выполнения задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задачи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления задачи')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def clean(self):
        """Проверка, что дата выполнения не в прошлом."""
        if self.due_date < timezone.now():
            raise ValidationError("Дата выполнения не может быть в прошлом.")

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комменатрия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE, verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')


