import graphene
from graphene import relay
from graphene_federation import key

from .utils import get_stars_from_rating
from ..core.fields import PrefetchingConnectionField

from ...book import models
from ..core.connection import CountableDjangoObjectType


class Book(CountableDjangoObjectType):
    reviews = PrefetchingConnectionField(
        lambda: Review, description="List of reviews for this book."
    )

    class Meta:
        description = (
            "A book object."
        )
        only_fields = [
            "id",
            "isbn",
            "title",
            "author",
            "genre",
        ]
        interfaces = [relay.Node]
        model = models.Book


class ReviewRatingStars(graphene.ObjectType):
    class Meta:
        description = (
            "Review rating star details"
        )

    full_stars = graphene.Int(
        description="Number of full stars in the review rating.",
        required=True)
    empty_stars = graphene.Int(
        description="Number of empty stars in the review rating.",
        required=True)
    has_half_star = graphene.Boolean(description="Boolean if the review has half star")


@key(fields="id")
class Review(CountableDjangoObjectType):
    rating_stars = \
        graphene.Field(ReviewRatingStars,
                       description="A break down of the stars "
                                   "of the review rating")

    class Meta:
        description = (
            "Represents a single review of book."
        )
        only_fields = [
            "id",
            "rating",
            "description",
            "book"
        ]
        interfaces = [relay.Node ]
        model = models.Review

    @staticmethod
    def resolve_rating_stars(root: models.Review, _info):
        full_stars, empty_stars, has_half_star = get_stars_from_rating(root.rating)
        return ReviewRatingStars(full_stars=full_stars,
                                 empty_stars=empty_stars,
                                 has_half_star=has_half_star)

