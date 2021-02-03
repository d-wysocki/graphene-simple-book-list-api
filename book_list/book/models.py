from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from ..core.models import SortableModel


class Book(SortableModel):
    isbn = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)

    objects = models.Manager()

    class Meta:
        ordering = ("sort_order", "title",)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_ordering_queryset(self):
        return Book.objects.all()


class ReviewManager(models.QuerySet):
    def create_from_data_with_isbn(self, review_data):
        book_found = False
        created = None
        review = None
        book_isbn = review_data.pop("isbn")
        book = Book.objects.filter(isbn=book_isbn).first()
        if book:
            book_found = True
            review_data["book"] = book
            review, created = self.get_or_create(**review_data)
            return book_found, review, created
        else:
            return book_found, review, created


class Review(models.Model):
    book = models.ForeignKey(
        Book, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    description = models.TextField(blank=True, null=True)

    objects = ReviewManager.as_manager()

    def __str__(self) -> str:
        return f"{self.rating} star rating review on {self.book}"

