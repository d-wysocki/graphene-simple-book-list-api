import django_filters
import graphene
from graphene import InputField

from ...tests.utils import get_graphql_content, get_graphql_content_from_response
from ..types import FilterInputObjectType

from ....book.models import Book
from ..utils import (
    clean_seo_fields,
    get_duplicated_values,
    snake_to_camel_case,
)


def test_clean_seo_fields():
    title = "lady title"
    description = "fantasy description"
    data = {"seo": {"title": title, "description": description}}
    clean_seo_fields(data)
    assert data["seo_title"] == title
    assert data["seo_description"] == description


def test_snake_to_camel_case():
    assert snake_to_camel_case("test_camel_case") == "testCamelCase"
    assert snake_to_camel_case("testCamel_case") == "testCamelCase"
    assert snake_to_camel_case(123) == 123


def test_require_pagination(api_client):
    query = """
    query {
        books {
            edges {
                node {
                    title
                }
            }
        }
    }
    """
    response = api_client.post_graphql(query)
    content = get_graphql_content_from_response(response)
    assert "errors" in content
    assert content["errors"][0]["message"] == (
        "You must provide a `first` or `last` value to properly paginate the "
        "`books` connection."
    )


def test_total_count_query(api_client, book):
    query = """
    query {
        books {
            totalCount
        }
    }
    """
    response = api_client.post_graphql(query)
    content = get_graphql_content(response)
    assert content["data"]["books"]["totalCount"] == Book.objects.count()


def test_filter_input():
    class TestBookFilter(django_filters.FilterSet):
        search = django_filters.CharFilter()

        class Meta:
            model = Book
            fields = {"search": ["contains"]}

    class TestFilter(FilterInputObjectType):
        class Meta:
            filterset_class = TestBookFilter

    test_filter = TestFilter()
    fields = test_filter._meta.fields

    assert "search" in fields
    search = fields["search"]
    assert isinstance(search, InputField)
    assert search.type == graphene.String


def test_get_duplicated_values():
    values = ("a", "b", "a", 1, 1, 1, 2)

    result = get_duplicated_values(values)

    assert result == {"a", 1}
