# Standard Library Imports
import datetime
import hashlib

# Third-party imports
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action, permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

# Django imports
from django.contrib.auth.models import User, update_last_login
from django.conf import settings
from django.contrib.auth.models import User, update_last_login
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.authentication import (
    get_authorization_header,
    SessionAuthentication,
)
import six
import json
import random
import string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from api.models import *
from config.utils import CustomSchema
import coreapi
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import grammar_correction
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GrammarCorrectionSerializer


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def health_check(request):
    """
    Endpoint for health check.
    """
    return HttpResponse("OK")


@permission_classes((AllowAny,))
class GrammarCorrectionView(APIView):
    serializer_class = GrammarCorrectionSerializer  # 시리얼라이저 지정

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            text_to_correct = serializer.validated_data.get('text', '')

            if not text_to_correct:
                return Response({'error': 'Text to correct is required.'}, status=status.HTTP_400_BAD_REQUEST)

            corrected_text = grammar_correction(text_to_correct)
            return Response({'corrected_text': corrected_text}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
