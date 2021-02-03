import json
import logging

import graphene
import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import reverse
from django.test.client import MULTIPART_CONTENT, Client

from ...tests.utils import flush_post_commit_hooks
from ..views import handled_errors_logger, unhandled_errors_logger
from .utils import assert_no_permission

API_PATH = reverse("api")
ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"


class ApiClient(Client):
    """GraphQL API client."""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", AnonymousUser())
        app = kwargs.pop("app", None)
        self._user = None
        self.token = None
        self.user = user
        super().__init__(*args, **kwargs)

    def _base_environ(self, **request):
        environ = super()._base_environ(**request)
        if not self.user.is_anonymous:
            environ["HTTP_AUTHORIZATION"] = f"JWT {self.token}"
        elif self.app_token:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {self.app_token}"
        return environ

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def post(self, data=None, **kwargs):
        """Send a POST request.

        This wrapper sets the `application/json` content type which is
        more suitable for standard GraphQL requests and doesn't mismatch with
        handling multipart requests in Graphene.
        """
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)
        kwargs["content_type"] = "application/json"
        return super().post(API_PATH, data, **kwargs)

    def post_graphql(
        self,
        query,
        variables=None,
        permissions=None,
        check_no_permissions=True,
        **kwargs,
    ):
        """Dedicated helper for posting GraphQL queries.

        Sets the `application/json` content type and json.dumps the variables
        if present.
        """
        data = {"query": query}
        if variables is not None:
            data["variables"] = variables
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)
        kwargs["content_type"] = "application/json"

        if permissions:
            if check_no_permissions:
                response = super().post(API_PATH, data, **kwargs)
                assert_no_permission(response)
            if self.app:
                self.app.permissions.add(*permissions)
            else:
                self.user.user_permissions.add(*permissions)
        result = super().post(API_PATH, data, **kwargs)
        flush_post_commit_hooks()
        return result

    def post_multipart(self, *args, permissions=None, **kwargs):
        """Send a multipart POST request.

        This is used to send multipart requests to GraphQL API when e.g.
        uploading files.
        """
        kwargs["content_type"] = MULTIPART_CONTENT

        if permissions:
            response = super().post(API_PATH, *args, **kwargs)
            assert_no_permission(response)
            self.user.user_permissions.add(*permissions)
        return super().post(API_PATH, *args, **kwargs)


@pytest.fixture
def app_api_client(app):
    return ApiClient(app=app)


@pytest.fixture
def staff_api_client(staff_user):
    return ApiClient(user=staff_user)


@pytest.fixture
def superuser_api_client(superuser):
    return ApiClient(user=superuser)


@pytest.fixture
def user_api_client(customer_user):
    return ApiClient(user=customer_user)


@pytest.fixture
def api_client():
    return ApiClient(user=AnonymousUser())


@pytest.fixture
def schema_context():
    params = {"user": AnonymousUser()}
    return graphene.types.Context(**params)


class LoggingHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []

    def emit(self, record: logging.LogRecord):
        exc_type, exc_value, _tb = record.exc_info
        self.messages.append(
            f"{record.name}[{record.levelname.upper()}].{exc_type.__name__}"
        )


@pytest.fixture
def graphql_log_handler():
    log_handler = LoggingHandler()

    unhandled_errors_logger.addHandler(log_handler)
    handled_errors_logger.addHandler(log_handler)

    return log_handler

