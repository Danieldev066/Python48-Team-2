from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    deadline_after = filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')

    class Meta:
        model = Task
        fields = {
            'project': ['exact'],
            'priority': ['exact'],
            'completed': ['exact'],
            'assignee': ['exact'],
            'tags': ['exact'],
        }