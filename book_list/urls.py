from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .graphql.api import schema
from .graphql.views import GraphQLView
from .core import views


urlpatterns = [
    url(r"^graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="api"),
    url(r"^", views.home, name="home"),
]

