import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from ....book.models import Book, Review


class Command(BaseCommand):
    help = "Populate database with books and reviews " \
           "from fixtures/books.csv and  fixtures/reviews.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "--createsuperuser",
            action="store_true",
            dest="createsuperuser",
            default=False,
            help="Create admin account",
        )

    def make_database_faster(self):
        """Sacrifice some of the safeguards of sqlite3 for speed.

        Users are not likely to run this command in a production environment.
        They are even less likely to run it in production while using sqlite3.
        """
        if "sqlite3" in connection.settings_dict["ENGINE"]:
            cursor = connection.cursor()
            cursor.execute("PRAGMA temp_store = MEMORY;")
            cursor.execute("PRAGMA synchronous = OFF;")

    def handle(self, *args, **options):
        self.make_database_faster()
        books_path = "fixtures/books.csv"
        reviews_path = "fixtures/reviews.csv"

        has_reviews = os.path.exists(reviews_path)
        has_books = os.path.exists(books_path)

        if not (has_books and has_reviews):
            raise CommandError("Book and reviews fixture data is "
                               "required to populate data base")

        heading_row_index = 0
        loaded_books_count = 0
        loaded_reviews_count = 0
        with open(books_path) as f:
            reader = csv.reader(f)
            headings = None
            review_csv_list = list(reader)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Found {len(review_csv_list) - 1} books in fixture data'
                )
            )
            for row_index in range(len(review_csv_list)):
                if row_index == heading_row_index:
                    headings = list(
                        filter(None, review_csv_list[row_index][0].
                               replace(" ", "").lower().split(";")
                               )
                    )
                else:
                    values = list(
                        filter(None, review_csv_list[row_index][0].
                               replace(" ", "").split(";")
                               )
                    )
                    book_data = dict(zip(headings, values))
                    book, created = Book.objects.get_or_create(**book_data)
                    if created:
                        loaded_books_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Loaded {book} into database'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'{book} already in database so skipped'
                            )
                        )

        with open(reviews_path) as f:
            reader = csv.reader(f)
            headings = None
            review_csv_list = list(reader)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Found {len(review_csv_list) - 1} reviews in fixture data'
                )
            )
            for row_index in range(len(review_csv_list)):
                if row_index == heading_row_index:
                    headings = list(filter(None, review_csv_list[row_index][0].
                                           replace(" ", "").lower().split(";")))
                else:
                    values = list(filter(None, review_csv_list[row_index][0].
                                         replace(" ", "").split(";")))
                    review_data = dict(zip(headings, values))
                    book_isbn = review_data.get("isbn")
                    book_found, review, created = Review.objects.create_from_data_with_isbn(review_data)

                    if not book_found:
                        self.stdout.write(
                            self.style.WARNING(
                                f'No book found with isbn {book_isbn}'
                            )
                        )
                        continue
                    if created:
                        loaded_reviews_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Loaded {review} into database'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'{review} already in database so skipped'
                            )
                        )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully populated the database with '
                f'{loaded_books_count} new book(s) and '
                f'{loaded_reviews_count} new review(s) '
                f'from the fixtures data'
            )
        )


