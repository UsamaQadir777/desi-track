from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback


def _plain_detail(value):
    if isinstance(value, ErrorDetail):
        return str(value)
    if isinstance(value, list):
        return [_plain_detail(item) for item in value]
    if isinstance(value, dict):
        return {key: _plain_detail(item) for key, item in value.items()}
    return value


def _error_code(exc, response):
    if isinstance(exc, ValidationError):
        return "validation_error"
    if isinstance(exc, Http404):
        return "not_found"
    if isinstance(exc, PermissionDenied):
        return "permission_denied"
    if isinstance(exc, APIException):
        return getattr(exc, "default_code", "api_error")
    if response is not None:
        return "api_error"
    return "internal_server_error"


def _message(details, fallback):
    if isinstance(details, dict):
        detail = details.get("detail")
        if detail:
            return str(detail)
        return fallback
    if isinstance(details, list):
        return fallback
    return str(details) if details else fallback


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        set_rollback()
        return Response(
            {
                "error": {
                    "code": _error_code(exc, response),
                    "message": "An unexpected server error occurred.",
                    "details": {},
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    details = _plain_detail(response.data)
    code = _error_code(exc, response)
    response.data = {
        "error": {
            "code": code,
            "message": _message(details, "Validation failed." if code == "validation_error" else "Request failed."),
            "details": details,
        }
    }
    return response
