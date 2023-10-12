# Standard Library Imports
from datetime import timedelta
from functools import reduce
import json

# Third-party imports
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

# Django imports
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, F

# Local imports
from api.models import Answer, GrammarContent, Category, User, Profile  # 실제 모델 경로에 따라 수정

# SNS 회원가입 후 DB 연동
@swagger_auto_schema(
    method="POST",
    operation_description="Create SNS user and link to DB",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "sns_id": openapi.Schema(type=openapi.TYPE_STRING, description="SNS ID of the user"),
            "sns_type": openapi.Schema(type=openapi.TYPE_STRING, description="SNS type"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of the user"),
        },
    ),
    responses={201: "User profile created successfully"},
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def create_sns_user(request):
    """
    Create a new SNS user and link to the database.
    """
    try:
        sns_id = request.data.get("sns_id")
        sns_type = request.data.get("sns_type")
        email = request.data.get("email")  # 추가된 email 정보를 받음
        # 기존 User 모델의 email 필드에 이메일 저장
        user, created = User.objects.get_or_create(username=sns_id, defaults={"email": email})
        profile, profile_created = Profile.objects.get_or_create(user=user, sns_id=sns_id,sns_type=sns_type)
        
        return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id})
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


# SNS 로그인 후 DB에서 유저 정보 연결
@swagger_auto_schema(
    method="GET",
    operation_description="Get SNS user profile",
    manual_parameters=[
        openapi.Parameter(
            name="sns_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="SNS ID of the user",
        ),
    ],
    responses={200: "Successful response description here"},
)
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_sns_user(request, sns_id):
    """Retrieve an SNS user's profile from the database."""
    try:
        user = User.objects.get(username=sns_id)
        return Response(status=status.HTTP_200_OK, data={"user_id": user.id})
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "User does not exist"})
    

@swagger_auto_schema(
    method="GET",
    operation_description="Get the last subcategory for a user",
    manual_parameters=[
        openapi.Parameter(
            name="user_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="User ID",
        ),
    ],
    responses={200: "Successful response description here"},
)
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_last_sub_category(request, user_id):
    try:
        last_answer = Answer.objects.filter(user_id=user_id).latest('answered_at')
        last_grammar_content = GrammarContent.objects.get(id=last_answer.grammar_content_id)
        last_category = Category.objects.get(id=last_grammar_content.category_id)
        
        if last_category.level == 3:
            redirect_url = f"/sub_category/{last_category.id}/"
            return JsonResponse({"redirect_to": redirect_url})
        
        return JsonResponse({"redirect_to": "/main_category/"})
        
    except Answer.DoesNotExist:
        return JsonResponse({"redirect_to": "/main_category/"})
        

@swagger_auto_schema(
    method="GET",
    operation_description="Get answer statistics for the last 7 days",
    responses={200: "Successful response description here"},
)
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_answer_stats(request, user_id):
    try:
        # Try to get the user object
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        # Return an error response if the user is not found
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "User does not exist"})

    # 7일 전 날짜와 시간을 구합니다.
    past_week_date = timezone.now() - timedelta(days=7)
    past_week_date = past_week_date.replace(hour=0, minute=1, second=0, microsecond=0)

    # 현재 시간을 구합니다.
    current_time = timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)

    # 해당 사용자의 최근 7일간의 답변을 필터링합니다.
    answer_results = Answer.objects.filter(
        user=user,
        answered_at__range=(past_week_date, current_time)
    )

    total_count = answer_results.count()
    correct_count = answer_results.filter(is_correct=True).count()

    if total_count == 0:
        return Response({
            "message": "No answer data available",
            "correct": 0,
            "incorrect": 0,
            "correct_rate": 0
        })

    incorrect_count = total_count - correct_count
    correct_rate = (correct_count / total_count) * 100

    return Response({
        "correct": correct_count,
        "incorrect": incorrect_count,
        "correct_rate": correct_rate
    })


ITEM_COUNT_PER_PAGE = 30
SCHEMA_FILED_EXCEPT = [
    "page",
    # "filter",
    "id",
    "count_per_page",
    "depth",
    "logic",
    "order_by",
    "ignore[]",
    "content_type",
    "prefetch",
]
CHAIN_FILTER = [
    "startswith",
    "endwith",
    "lte",
    "gte",
    "gt",
    "lt",
    "contains",
    "icontains",
    "exact",
    "iexact",
]

def getSerializer(modelClass):
    class_name = modelClass.__name__
    class ApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = modelClass
            fields = "__all__"
            ref_name = f"{class_name}API"  # 고유한 ref_name 설정

    return ApiSerializer



def readQuery(request, key):
    if "[]" in key:
        value = request.GET.get(key, "[]")
        if value == "[]":
            value = [-1]
        elif value.startswith("["):
            value = json.loads(value)
        else:
            value = request.GET.getlist(key)
        key = key.replace("[]", "")
    elif key.endswith("__not"):
        k = key.replace("__not", "")
        value = request.GET.get(key)
        return ~Q(**{k: value})
    else:
        value = request.GET.get(key)
        if value == "true":
            value = True
        elif value == "false":
            value = False
    return Q(**{key: value})


def applyOption(request, queryset):
    op = request.GET.get("filter")
    logic = request.GET.get("logic")
    where = [Q()]
    where__and = [Q()]
    used_keys = []
    if logic:
        keys = logic.split("__OR__")
        for key in keys:
            used_keys.append(key)
            where.append(readQuery(request, key))
    params = {}
    for key in request.GET:
        if key in SCHEMA_FILED_EXCEPT or key in used_keys:
            continue
        if key == "filter" and op is not None:
            params = json.loads(op)
        else:
            where__and.append(readQuery(request, key))

    queryset = queryset.filter(
        reduce(lambda x, y: x | y, where),
        reduce(lambda x, y: x & y, where__and),
    ).distinct()

    if len(params) != 0:
        queryset = queryset.filter(**params).distinct()

    return queryset

def my_note(request):
            return render(request, 'my_note.html')
        
def getViewSet(modelClass):
    # @permission_classes((IsAuthenticatedOrReadOnly,))
    # @authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
    @permission_classes(
    [
        AllowAny,
    ]
    )
    # @authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
    class ApiViewSet(viewsets.ModelViewSet):
        queryset = modelClass.objects.all().order_by("-id")
        serializer_class = getSerializer(modelClass)
        def list(self, request):
            page = request.GET.get("page")
            depth = request.GET.get("depth")
            count = request.GET.get("count_per_page")
            order = request.GET.get("order_by")
            ignore = request.GET.get("ignore[]")
            if ignore:
                ignore = request.GET.getlist("ignore[]")
            else:
                ignore = []
            queryset = applyOption(request, self.queryset)
            if order:
                queryset = queryset.order_by(*order.split(","))
            if page:
                res = applyPagination(
                    queryset, self.serializer_class, page, count, depth, ignore
                )
            else:
                res = []
                if depth:  # Deprecated
                    for item in queryset.all():
                        res.append(applyDepth(item, int(depth), ignore))
                else:
                    res = self.serializer_class(queryset, many=True).data
            return Response(res, status=status.HTTP_200_OK)

        def update(self, request, *args, **kwargs):
            partial = True
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

    return ApiViewSet


def applyPagination(queryset, serializer_class, page, count, depth, ignore):
    count_val = int(count) if count else ITEM_COUNT_PER_PAGE
    paginator = Paginator(queryset, count_val)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    output = []
    if depth:
        for item in items:
            output.append(applyDepth(item, int(depth), ignore))
    else:
        output = serializer_class(items, many=True).data
    res = {
        "items": output,
        "total_page": paginator.num_pages,
        "total": paginator.count,
    }
    return res


def applyDepth(item, depth, ignore):
    if item is None:
        return None
    if depth == -1:
        return item.id
    data = getSerializer(item.__class__)(item).data
    for field in item.__class__._meta.get_fields():
        if field.name in ignore:
            continue
        if field.many_to_one or field.one_to_one:
            if not hasattr(item, field.name):
                continue
            data[field.name] = applyDepth(getattr(item, field.name), depth - 1, ignore)
        elif field.many_to_many:
            if not hasattr(item, field.name):
                continue
            data[field.name] = []
            for m2m_item in getattr(item, field.name).all():
                data[field.name].append(applyDepth(m2m_item, depth - 1, ignore))
    return data