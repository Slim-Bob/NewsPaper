import django_filters
from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category
from datetime import timedelta

from django import forms

class PostsSearchFilter(FilterSet):
    titels = django_filters.CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )

    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'
    )

    create_date_time = django_filters.DateTimeFilter(
        field_name='create_date_time',
        label='Позже даты',
        lookup_expr='gt',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            # 'title': ['icontains'],
            # 'type': ['gt'],
        }
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     models.BooleanField: {
        #         'filter_class': django_filters.BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': forms.CheckboxInput,
        #         },
        #     },
        # }