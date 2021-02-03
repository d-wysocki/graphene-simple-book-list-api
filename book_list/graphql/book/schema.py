import graphene

from ..core.fields import FilterInputConnectionField
from .filters import BookFilterInput
from .resolvers import resolve_book, resolve_books
from .sorters import BookSortingInput
from .types import Book


class BookQueries(graphene.ObjectType):
    book = graphene.Field(
        Book,
        id=graphene.Argument(graphene.ID, description="ID of the book."),
        isbn=graphene.String(description="The isbn of the book."),
        description="Look up a book by ID or isbn.",
    )
    books = FilterInputConnectionField(
        Book,
        sort_by=BookSortingInput(description="Sort books."),
        filter=BookFilterInput(description="Filtering options for books."),
        description="List of the books in the book collection.",
    )

    def resolve_book(self, info, id=None, isbn=None):
        return resolve_book(info, id, isbn)

    def resolve_books(self, info, **kwargs):
        return resolve_books(info, **kwargs)


class BookMutations(graphene.ObjectType):
    pass
