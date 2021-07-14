from django.http import JsonResponse


def error_404(request, exception):
    message = 'The Endpoint is not found'
    response = JsonResponse(data={"detail": message, "status_code": 404})
    response.status_code = 404
    return response


def error_500(request):
    message = 'Server internal error'
    response = JsonResponse(data={"detail": message, "status_code": 500})
    response.status_code = 500
    return response
