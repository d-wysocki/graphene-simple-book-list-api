import os

from django.template.response import TemplateResponse


def home(request):
    api_url = os.environ.get("API_URL", "/graphql/")
    return TemplateResponse(
        request,
        "home/index.html",
        {"api_url": api_url, },
    )
