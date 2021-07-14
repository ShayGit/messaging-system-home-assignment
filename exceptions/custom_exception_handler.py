from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        response.data = {"detail": response.data}
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
