import graphene

from ..core.types import SortInputObjectType


class BookSortField(graphene.Enum):
    TITLE = ["title", "gerne"]
    GENRE = ["genre", "title"]
    ISBN = ["isbn", "title"]

    @property
    def description(self):
        if self.name in BookSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort books by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class BookSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = BookSortField
        type_name = "books"
