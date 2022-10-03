import django_filters
from .models import OneTimeCode


class OneTimeCodeFilter(django_filters.Filter):
    class Meta:
        model = OneTimeCode
        fields = ['code']
