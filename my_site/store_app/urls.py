from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoryListAPIView, ProjectViewSet, TagViewSet,
    TaskListCreateAPIView, TaskDetailAPIView,
    SubtaskViewSet, TaskFileViewSet, CommentViewSet,
    FavoriteAPIView, FavoriteItemViewSet
)

router = routers.DefaultRouter()
router.register(r'project', ProjectViewSet)
router.register(r'tag', TagViewSet)
router.register(r'subtask', SubtaskViewSet)
router.register(r'task_file', TaskFileViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'favorite_item', FavoriteItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('task/', TaskListCreateAPIView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('favorite/', FavoriteAPIView.as_view(), name='favorite'),
]