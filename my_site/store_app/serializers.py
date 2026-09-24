from rest_framework import serializers
from .models import (
    UserProfile, Category, Project, Tag, Task,
    Subtask, TaskFile, Comment, Favorite, FavoriteItem
)


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'status']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_img']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'task', 'title', 'completed']


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'task', 'file']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'text', 'created_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    tasks_count = serializers.SerializerMethodField()
    completed_percent = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'description', 'category',
                  'owner', 'created_date', 'tasks_count', 'completed_percent']

    def get_tasks_count(self, obj):
        return obj.get_tasks_count()

    def get_completed_percent(self, obj):
        return obj.get_completed_percent()

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'completed',
                  'deadline', 'project', 'tags', 'progress', 'overdue']

    def get_progress(self, obj):
        return obj.get_progress()

    def get_overdue(self, obj):
        return obj.is_overdue()


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    files = TaskFileSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'priority',
                  'deadline', 'created_date', 'project', 'assignee', 'tags',
                  'subtasks', 'files', 'comments',
                  'progress', 'comments_count', 'overdue']

    def get_progress(self, obj):
        return obj.get_progress()

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def get_overdue(self, obj):
        return obj.is_overdue()


class FavoriteItemSerializer(serializers.ModelSerializer):
    task = TaskListSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), write_only=True, source='task'
    )

    class Meta:
        model = FavoriteItem
        fields = ['id', 'task', 'task_id']


class FavoriteSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True,)