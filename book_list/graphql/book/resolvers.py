import graphene

from ...book import models


def resolve_book(info, global_book_id=None, isbn=None):
    assert global_book_id or isbn, "No book ID or slug provided."

    if isbn is not None:
        book = models.Book.objects.filter(isbn=isbn).first()
    else:
        _type, book_pk = graphene.Node.from_global_id(global_book_id)
        book = models.Book.objects.filter(pk=book_pk).first()
    return book


def resolve_books(_info, **_kwargs):
    return models.Book.objects.all()
