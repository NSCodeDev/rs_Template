import django_filters
from core.models.base import BaseModel


class BaseFilter(django_filters.FilterSet):
    """Filter for fields in BaseModel"""

    created_at = django_filters.DateTimeFilter(field_name='created_at')
    modified_at = django_filters.DateTimeFilter(field_name='modified_at')
    deleted_at = django_filters.DateTimeFilter(field_name='deleted_at')
    
    created_by = django_filters.UUIDFilter(field_name='created_by', lookup_expr='exact')
    modified_by = django_filters.UUIDFilter(field_name='modified_by', lookup_expr='exact')
    deleted_by = django_filters.UUIDFilter(field_name='deleted_by', lookup_expr='exact')
    
    is_deleted = django_filters.BooleanFilter(field_name='is_deleted', lookup_expr='exact')
    is_active = django_filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    
    class Meta:
        abstract = True
        fields = {
            'created_at': ['lt', 'gt', 'exact'],
            'modified_at': ['lt', 'gt', 'exact'],
            'deleted_at': ['lt', 'gt', 'exact'],
        }
