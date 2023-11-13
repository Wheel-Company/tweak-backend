# Third-party imports
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


# Define the health_check endpoint
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check():
    """
    Endpoint for health check.
    """
    return HttpResponse("OK")