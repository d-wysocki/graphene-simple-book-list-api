import pytest

from ...tests.utils import get_graphql_content
from ....book.models import Book

BOOKS = [
    {"isbn": "9788366436572", "title": "Intern", "author": "Alicja Sinicka", "genre": "Crime"},
    {"isbn": "9788381257978", "title": "In the Woods", "author": "Harlan Coben", "genre": "Thriller"},
    {"isbn": "9788366553798", "title": "RZNiW housing estate", "author": "Remigiusz Mróz", "genre": "Crime"},
    {"isbn": "9788380087583", "title": "The Ballad of Birds and Snakes", "author": "Suzanne Collins",
     "genre": "Youth Literature"},
    {"isbn": "9788381783392", "title": "Risk of gangster", "author": "Anna Wolf", "genre": "Literature of manners"},
]

# reviews = [
#     {"isbn": "9788366436572", "title": "Intern", "author": "Alicja Sinicka", "genre": "Crime"},
#     {"isbn": "9788381257978", "title": "In the Woods", "author": "Harlan Coben", "genre": "Thriller"},
#     {"isbn": "9788366553798", "title": "RZNiW housing estate", "author": "Remigiusz Mróz", "genre": "Crime"},
#     {"isbn": "9788380087583", "title": "The Ballad of Birds and Snakes", "author": "Suzanne Collins",
#      "genre": "Youth Literature"},
#     {"isbn": "9788381783392", "title": "Risk of gangster", "author": "Anna Wolf", "genre": "Literature of manners"},
# ]


@pytest.mark.parametrize(
    "book_filter, count",
    [
        ({"search": "Intern"}, 1),
        ({"search": "In"}, 3),
        ({"search": "Ballad"}, 1),
        ({"search": "RZNiW"}, 1),
        ({"search": "gangster"}, 1),
    ],
)
def test_books_query_search_title_with_filter(
        book_filter, count, user_api_client
):
    query = """
        query ($filter: BookFilterInput) {
            books(first: 5, filter:$filter) {
                totalCount
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """

    for book_input_data in BOOKS:
        Book.objects.create(book_input_data)
    variables = {"filter": book_filter}
    response = user_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    assert content["data"]["books"]["totalCount"] == count


BOOK_QUERY = """
    query BookQuery($id: ID, $isbn: String) {
        book(id: $id, isbn: $isbn) {
            title
            isbn
        }
    }
"""


def test_query_book_by_isbn(user_api_client, book, isbn):

    # query by ID
    variables = {"isbn": isbn}
    response = user_api_client.post_graphql(BOOK_QUERY, variables)
    content = get_graphql_content(response)
    book_data = content["data"]["book"]
    assert book_data is not None


def test_paginate_books(user_api_client, book):
    book.is_published = True
    data_02 = BOOKS[1]
    data_03 = BOOKS[2]

    Book.objects.create(**data_02)
    Book.objects.create(**data_03)
    query = """
        query BooksQuery {
            books(first: 2) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
        """
    response = user_api_client.post_graphql(query)
    content = get_graphql_content(response)
    books_data = content["data"]["books"]
    assert len(books_data["edges"]) == 2
