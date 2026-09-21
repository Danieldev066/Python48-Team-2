from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


STATUS_CHOICES = (
    ('beginner', 'beginner'),
    ('active', 'active'),
    ('pro', 'pro'),
)

PRIORITY_CHOICES = (
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high'),
)


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(70)],
        null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='beginner')
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_img = models.ImageField(upload_to='category_img/', null=True, blank=True)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    created_date = models.DateTimeField(auto_now_add=True)

    def get_tasks_count(self):
        return self.tasks.count()

    def get_completed_percent(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        completed = self.tasks.filter(completed=True).count()
        return round(completed * 100 / total, 1)

    def __str__(self):
        return f'{self.category.category_name} - {self.project_name}'


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag_name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_tasks'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')

    def get_progress(self):
        total = self.subtasks.count()
        if total == 0:
            return 0
        done = self.subtasks.filter(completed=True).count()
        return round(done * 100 / total, 1)

    def get_comments_count(self):
        return self.comments.count()

    def is_overdue(self):
        if self.deadline and not self.completed:
            return self.deadline < timezone.now()
        return False

    def __str__(self):
        return self.title


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task.title} - {self.title}'


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='task_files/')

    def __str__(self):
        return f'file - {self.task.title}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.task.title}'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return f'favorite - {self.user.username}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='items')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('favorite', 'task')

    def __str__(self):
        return self.task.title
