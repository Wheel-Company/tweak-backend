import datetime
import hashlib
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
from backend.utils import CustomSchema
import coreapi
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "is_superuser",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )
        if "email" in validated_data:
            user.email = validated_data["email"]
        if "groups" in validated_data:
            user.groups = validated_data["groups"]
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        if type(user) == ReturnDict:
            return (
                six.text_type(user["id"]) + six.text_type(timestamp)
            ) + six.text_type(user["is_active"])
        else:
            return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(
                user.is_active
            )


account_activation_token = AccountActivationTokenGenerator()


class AccountResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.last_login)
        )


account_reset_token = AccountResetTokenGenerator()


def activate(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        print("activate user : ", user.username, request.GET, request)
        user.is_active = True
        user.save()
        account = AccountItems(
            user=user,
        )
        account.save()
        return HttpResponseRedirect("/api-auth/login")
    else:
        return HttpResponse("invalid access")


def randomizeStr(len):
    rand_str = ""
    n = 10
    if len:
        n = len
    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase + string.digits))
    return rand_str


def verify(request):
    user = User.objects.get(username=request.GET.get("username"))
    validate = check_password(request.GET.get("password"), user.password)
    if validate is True:
        return JsonResponse({"result": True})
    return JsonResponse({"result": False})


@csrf_exempt
@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def send_validation_mail(request):
    email = request.GET.get("email")
    if email:
        current_site = get_current_site(request)
        code = randomizeStr(8)
        message = render_to_string(
            "account/validation_email.html",
            {"context": request.GET.get("context").replace("@code", code)},
        )
        email = EmailMessage(request.GET.get("title"), message, to=[email])
        email.send()
        return JsonResponse({"result": "ok", "code": code})
    return JsonResponse({"result": "fail"})


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def send_change_mail(request):
    user = request.user
    if user.is_authenticated:
        account = AccountItems.objects.get(user=user)
        alter_type = request.GET.get("type")
        email = user.email
        if alter_type == "email":
            email = account.sub_email
        code = randomizeStr(8)
        message = render_to_string(
            "account/validation_email.html",
            {"context": request.GET.get("context").replace("@code", code)},
        )
        email = EmailMessage(request.GET.get("title"), message, to=[email])
        email.send()
        return JsonResponse({"result": "ok", "code": code})
    return JsonResponse({"result": "fail"})


@csrf_exempt
def send_reset_mail(request):
    if request.method == "GET":
        email = request.GET.get("email")
        username = request.GET.get("username")
        if email:
            current_site = get_current_site(request)
            try:
                user = User.objects.get(username=username, email=email)
                print(email, user)
                # user_item = AccountUserItem.objects.get(user=user)
                domain = current_site.domain.replace("http://", "https://")
                message = render_to_string(
                    "account/password_reset_email.html",
                    {
                        # 'user_item': user_item,
                        "domain": domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk))
                        .encode()
                        .decode(),
                        "token": account_reset_token.make_token(user),
                    },
                )
                subject, from_email, to = (
                    "[Ai-Bgm] 비밀번호 변경",
                    "customer.service@juice.co.kr",
                    email,
                )
                text_content = strip_tags(message)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(message, "text/html")
                msg.send()
                # return JsonResponse({'result': 'ok'}, status=200)
                return HttpResponse("귀하의 이메일로 비밀번호 변경 이메일을 보냈습니다.")
            except:
                return JsonResponse({"result": "Not Found"}, status=404)

    elif request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        uid = force_str(urlsafe_base64_decode(body["uid"]))
        user = User.objects.get(pk=uid)
        if user is not None and account_reset_token.check_token(user, body["token"]):
            user.set_password(body["password"])
            user.save()
            return JsonResponse({"result": "ok"}, status=200)
    return JsonResponse({"result": "Unauthorized"}, status=401)


def reset(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    # body = json.loads(request.body.decode('utf-8'))
    # print('reset : ',user, body, body['token']), body('password')
    if user is not None and account_reset_token.check_token(user, token):
        # user.password = True
        new_pw = randomizeStr(8)
        print("new pass : ", new_pw, user.password)
        user.set_password(new_pw)
        user.save()
        return HttpResponse("Your new Password  : %s" % new_pw)
    else:
        return HttpResponse("invalid access")


def edit(request):
    if request.method == "GET":
        return JsonResponse({"result": "Wrong get method caller"})
    elif request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        print(body, request.body)
        return HttpResponse("good")


def is_active(request, pk):
    user = User.objects.get(pk=pk)
    return HttpResponse(
        json.dumps({"is_active": user.is_active}), content_type="application/json"
    )


@permission_classes((AllowAny,))
@authentication_classes((JSONWebTokenAuthentication,))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    # schema = CustomSchema({
    #     'list': [
    #         coreapi.Field('self', required=False, location='query',
    #                       type='string', description='get auth user data')
    #     ]
    # })

    def list(self, request):
        email = request.GET.get("email")
        if request.GET.get("user_self") == "true":
            if request.user.is_authenticated:
                serializer = self.serializer_class(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif email:
            out = {"email": False, "id": None}
            if email and User.objects.filter(email=email).count() > 0:
                out["email"] = True
                out["id"] = User.objects.filter(email=email)[0].id
            return Response(out, status=status.HTTP_200_OK)
        serializers = self.serializer_class(self.queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
        # return Response('')

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        marketing = request.data.get("marketing_agreement")
        company = request.data.get("company")
        name = request.data.get("name")
        sub_email = request.data.get("sub_email")
        phone = request.data.get("phone")

        company_code = request.data.get("company_code")
        company_name = request.data.get("company_name")
        profile_img = request.data.get("profile_img")
        if User.objects.filter(username=email).count() > 0:
            return Response({"result": "already exists"})

        user = User.objects.create(username=email, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()

        account = AccountItems.objects.create(user=user, name=name)
        account.sub_email = sub_email
        account.marketing_agreement = marketing
        account.name = name
        account.phone = phone
        if company_code is not None:
            account.company_code = company_code
        if company_name is not None:
            account.company_name = company_name

        if profile_img is not None:
            account.profile_img = profile_img
        account.save()
        return Response({"result": "success", "id": user.id})

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            account = AccountItems.objects.get(user=pk)
            return Response(
                {
                    "id": user.id,
                    "name": account.name,
                    "phone": account.phone,
                    "email": user.email,
                    "password": user.password,
                }
            )
        except AccountItems.DoesNotExist:
            return Response({"result": "Account Does not Exist"})

    def destroy(self, request, pk=None):
        user = User.objects.get(pk=pk)
        # if user.is_active == False or user.check_password('initial_password'):
        #     user.delete()
        #     return Response({'msg': 'success'})
        if request.user.id != int(pk):
            return Response({"msg": "not found"}, status=404)
        user.delete()
        return Response({"msg": "success"})

    def update(self, request, pk=None, *args, **kwargs):
        body = json.loads(request.body)
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        user = User.objects.get(pk=pk)
        if body.get("password"):
            user.set_password(body.get("password"))
        if body.get("email"):
            user.username = body.get("email")
            user.email = body.get("email")
        if body.get("username"):
            user.username = body.get("username")
            user.email = body.get("username")
        user.save()
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


# @permission_classes((AllowAny,))
# @authentication_classes((JSONWebTokenAuthentication,))
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

#     # schema = CustomSchema({
#     #     'list': [
#     #         coreapi.Field('self', required=False, location='query', type='string', description='get auth user data')
#     #     ]
#     # })

#     #mapping -> auth.User 로 검색해서 foreign key 로 account 정보 주기
#     def retrieve(self, request, pk=None):
#         email = request.GET.get('email')
#         try :
#             if email :
#                 user = User.objects.get(email=email)
#                 print('user : ', user, user.pk)
#                 account = AccountItems.objects.get(pk=user.pk)
#                 return Response({
#                     'user': account.user.id,
#                     'email': account.user.email,
#                     'phone': account.phone
#                 })
#             else :
#                 account = AccountItems.objects.get(pk=pk)
#                 return Response({
#                     'user': account.user.id,
#                     'email': account.user.email,
#                     'phone': account.phone
#                 })
#         except User.DoesNotExist :
#             return Response({'result ' : 'User does not exists'})
#         except AccountItems.DoesNotExist:
#             return Response({'result ' : "Account does not exists",})

#     def list(self, request):
#         username = request.GET.get('username')
#         email = request.GET.get('email')
#         if request.GET.get('self') == 'true':
#             if request.user.is_authenticated:
#                 serializer = self.serializer_class(request.user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_401_UNAUTHORIZED)
#         elif username:
#             out = {'username':False, 'email':False}
#             if User.objects.filter(username=username).count() > 0:
#                 out['username'] = True
#             if email and User.objects.filter(email=email).count() > 0:
#                 out['email'] = True
#             return Response(out, status=status.HTTP_200_OK)
#         serializers = self.serializer_class(self.queryset, many=True)
#         return Response(serializers.data, status=status.HTTP_200_OK)

#     def create(self, request):
#         response = super().create(request)
#         current_site = get_current_site(request)
#         message = render_to_string('account/user_activate_email.html', {
#             'user':response.data,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(response.data['id'])).encode().decode(),
#             'token': account_activation_token.make_token(response.data)
#         })
#         email = EmailMessage('Activation Mail', message, to=[response.data['email']])
#         email.send()
#         return response

#     def update(self, request, pk=None, *args, **kwargs):
#         body = json.loads(request.body)
#         partial = True
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         if(body.get('password')) :
#             user = User.objects.get(pk=pk)
#             user.set_password(body.get('password'))
#             user.save()
#         if getattr(instance, '_prefetched_objects_cache', None):
#         # If 'prefetch_related' has been applied to a queryset, we need to
#         # forcibly invalidate the prefetch cache on the instance.
#           instance._prefetched_objects_cache = {}
#         return Response(serializer.data)
