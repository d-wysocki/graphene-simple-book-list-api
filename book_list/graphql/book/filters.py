import django_filters

from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param
from ...book.models import Book


def filter_fields_containing_value(*search_fields: str):
    """Create a icontains filters through given fields on a given query set object."""

    def _filter_qs(qs, _, value):
        if value:
            qs = filter_by_query_param(qs, value, search_fields)
        return qs

    return _filter_qs


class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method=filter_fields_containing_value("title", )
    )

    class Meta:
        model = Book
        fields = ["search"]


class BookFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = BookFilter
