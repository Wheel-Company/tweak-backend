from django.http import JsonResponse
from rest_framework.status import is_success, is_client_error

class CustomResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Swagger와 관련된 URL은 예외 처리
        if request.path.startswith('/swagger/'):
            return self.get_response(request)

        # "/api/"로 시작하는 URL만 처리
        if request.path.startswith('/api'):
            response = self.get_response(request)

        if hasattr(response, 'data'):
            if is_success(response.status_code):
                data = {
                    "responseCode": response.status_code,
                    "responseMsg": "Success",
                    "result": response.data
                }
            elif is_client_error(response.status_code):
                data = {
                    "responseCode": response.status_code,
                    "responseMsg": "Fail",
                    "result": response.data
                }
            else:
                return response

            return JsonResponse(data)
        
        return response
