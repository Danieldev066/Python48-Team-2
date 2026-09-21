from django.contrib import admin


from django.contrib import admin
from .models import (
    UserProfile, Category, Project, Tag, Task,
    Subtask, TaskFile, Comment, Favorite, FavoriteItem
)


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'phone_number', 'status')
    search_fields = ('username', 'email')
    list_filter = ('status',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'category', 'owner', 'get_completed_percent')
    list_filter = ('category',)
    search_fields = ('project_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'completed', 'deadline', 'is_overdue')
    search_fields = ('title',)
    list_filter = ('priority', 'completed', 'project')
    filter_horizontal = ('tags',)
    inlines = (SubtaskInline, TaskFileInline, CommentInline)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (FavoriteItemInline,)


admin.site.register(Subtask)
admin.site.register(TaskFile)
admin.site.register(Comment)