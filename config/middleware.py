from django.http import JsonResponse
from rest_framework import status

class CustomResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # rest_framework.status의 상태 코드 상수를 활용
        self.status_messages = {
            status.HTTP_200_OK: "OK",
            status.HTTP_201_CREATED: "Created",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }

    def __call__(self, request):
        # Swagger와 관련된 URL은 예외 처리
        if request.path.startswith('/swagger/'):
            return self.get_response(request)

        # "/api/"로 시작하는 URL만 처리
        if request.path.startswith('/api'):
            response = self.get_response(request)

            if hasattr(response, 'data'):
                response_message = self.status_messages.get(response.status_code, "Unknown Status")
                data = {
                    "responseCode": response.status_code,
                    "responseMsg": response_message,
                    "result": response.data
                }
                return JsonResponse(data)

        return self.get_response(request)
