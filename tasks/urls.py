from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView, CommentUpdateView,
    CommentDeleteView, CommentLikeView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),  # головна сторінка
    path('task/create/', TaskCreateView.as_view(), name='task-create'),  # додати цей маршрут
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),  # для редагування
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),  # для видалення
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/like/', CommentLikeView.as_view(), name='comment-like'),
]
