

<div align="center">
  <h1>Book List Graphql API</h1>
</div>

<br>

<div align="center">
 Simple graphQl api for a list of books with their reviews
</div>

<br>

<br>

## Features

- **Graphql filter**: Search books by title using grapql filter inputs
- **Graphql playground**: A grapql playground environment for you to test your queries
- **SqlLite db**: Light weight and "portable" sqlite database
- **Management command**: Populate database from fixture csv data using custom django management command 

## Extra Features

- **Pagination**: Both books and their reviews can be paginated
- **List sortability**: Books can also be sorted using sorting input fields


## Installation

Book list app requires Python 3.8.

**1. Clone the repository:**
git clone https://github.com/thegleam/graphene-simple-book-list-api.git

**2. Install python requirements:**
cd book_list &&
pip install -r requirements.txt

**3. Handle migrations:**
python manage.py makemigrations &&
python manage.py migrate

**4. populate database:**
python manage.py populatedb

**5. runserver:**
python manage.py runserver

## Accessing the api

The api runs by default on:
http://127.0.0.1:8000/

Open the link on your web browser while the service is running.
Visit http://127.0.0.1:8000/graphql/ to access the graphql playground



