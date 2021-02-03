from graphene_federation import build_schema
from .book.schema import BookQueries


class Query(
    BookQueries,
):
    pass


schema = build_schema(Query)
