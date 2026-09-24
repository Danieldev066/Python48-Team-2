from rest_framework import generics, viewsets, permissions, serializers, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Project, Tag, Task, Subtask, TaskFile, Comment, Favorite, FavoriteItem
from .filters import TaskFilter
from .serializers import (
    CategorySerializer, ProjectSerializer, TagSerializer,
    TaskListSerializer, TaskSerializer, SubtaskSerializer,
    TaskFileSerializer, CommentSerializer,
    FavoriteSerializer, FavoriteItemSerializer
)


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'owner']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# ---- CRUD для задач с фильтрацией, поиском и сортировкой ----
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'created_date', 'priority']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskSerializer
        return TaskListSerializer


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task', 'completed']


class TaskFileViewSet(viewsets.ModelViewSet):
    queryset = TaskFile.objects.all()
    serializer_class = TaskFileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task', 'user']


class FavoriteAPIView(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        favorite, _ = Favorite.objects.get_or_create(user=request.user)
        return Response(self.get_serializer(favorite).data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return FavoriteItem.objects.none()
        return FavoriteItem.objects.filter(favorite__user=self.request.user)

    def perform_create(self, serializer):
        favorite, _ = Favorite.objects.get_or_create(user=self.request.user)
        task = serializer.validated_data['task']
        if FavoriteItem.objects.filter(favorite=favorite, task=task).exists():
            raise serializers.ValidationError('Задача уже в избранном')
        serializer.save(favorite=favorite)