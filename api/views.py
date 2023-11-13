# Standard Library Imports
import json
from datetime import timedelta
from functools import reduce

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
# Django imports
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Third-party imports
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Local imports
from api.models import (Answer, Category, Note, Profile,  # 실제 모델 경로에 따라 수정
                        User, WritingContent)
# Import your serializer for the Note model here
from config.serializers import NoteSerializer
from config.utils import CustomSchema, grammar_correction


@swagger_auto_schema(
    method="GET",
    operation_description="Get my note list",
    manual_parameters=[
        openapi.Parameter(
            name="user_id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="User ID to retrieve notes",
        ),
    ],
    responses={200: "Successful response description here"},
)
@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def get_note_list(request, user_id):
    """
    Retrieve a list of notes for a specific user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user to retrieve notes for.

    Returns:
        Response: The HTTP response containing the serialized note data.
    """
    # Rest of the function code...
    queryset = Note.objects.filter(user_id=user_id).order_by("-id")
    serializer = NoteSerializer(queryset, many=True)
    return Response(serializer.data)
    
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
        
        return JsonResponse(status=status.HTTP_201_CREATED, data={"user_id": user.id})
    except Exception as e:
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


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
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_last_sub_category(request, user_id):
    """
    Retrieve the last sub-category for a given user ID.

    Parameters:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user.

    Returns:
        JsonResponse: A JSON response containing the redirect URL.

    Raises:
        N/A
    """
    try:
        last_answer = Answer.objects.filter(user_id=user_id).latest('answered_at')
        last_writing_content = WritingContent.objects.get(id=last_answer.writing_content_id)
        last_category = Category.objects.get(id=last_writing_content.category_id)
        
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
    """
    Get answer statistics for the last 7 days.

    Parameters:
    - request: The request object.
    - user_id: The ID of the user.

    Returns:
    - A successful response with the answer statistics for the last 7 days.

    Raises:
    - Http404: If the user does not exist.
    """
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

@swagger_auto_schema(
    method="POST",
    operation_description="Correct grammar in text",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "text": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Text to correct grammar",
            ),
        },
    ),
    responses={200: "Successful response description here"},
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def grammar_correction_view(request):
    """
    Corrects the grammar of the given text.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response object containing the corrected text.

    Raises:
        ValueError: If the 'text' parameter is missing in the request data.

    """
    text_to_correct = request.data.get('text', '')

    if not text_to_correct:
        return Response({'error': 'Text to correct is required.'}, status=status.HTTP_400_BAD_REQUEST)

    corrected_text = grammar_correction(text_to_correct)
    return Response({'corrected_text': corrected_text}, status=status.HTTP_200_OK)
    
ITEM_COUNT_PER_PAGE = 30
SCHEMA_FILED_EXCEPT = [
    "page",
    "filter",
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
def addAllFieldToSchema(model, schema):
    """
    Add all fields from the model to the schema.

    Args:
        model: The model to extract fields from.
        schema: The schema to add the fields to.

    Returns:
        The modified schema.
    """
    # Rest of the function code...
    for field in model._meta.fields:
        name = field.__str__().split('.')[-1]
        # if name in SCHEMA_FILED_EXCEPT:
        #   continue
        schema.append(openapi.Parameter(name, openapi.IN_QUERY, description="", type=openapi.TYPE_INTEGER, required=False))
    return schema

def getSerializer(model_class):
    """
    Generate a serializer class for the given model class.

    Parameters:
        model_class (class): The model class to create the serializer for.

    Returns:
        class: The generated serializer class.

    Note:
        - The generated serializer class is a subclass of `serializers.ModelSerializer`.
        - The generated serializer class has a `Meta` inner class that specifies the model, fields, and ref_name.

    Example:
        >>> serializer = getSerializer(MyModel)
        >>> serialized_data = serializer(data=my_data)
        >>> serialized_data.is_valid()
        True
    """
    class_name = model_class.__name__
    class ApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = "__all__"
            ref_name = f"{class_name}API"  # 고유한 ref_name 설정

    return ApiSerializer



def readQuery(request, key):
    """
    Reads a query parameter from the given HTTP request and returns a Django Q object.

    Args:
        request (HttpRequest): The HTTP request object.
        key (str): The name of the query parameter to read.

    Returns:
        Q: A Django Q object representing the query.

    Raises:
        None.
    """
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
    """
    Apply option to the given queryset based on the request parameters.

    Args:
        request (HttpRequest): The HTTP request object.
        queryset (QuerySet): The queryset to apply options to.

    Returns:
        QuerySet: The modified queryset.

    Raises:
        None
    """
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

def generate_manual_parameters(modelClass):
    """
    Generate manual parameters for filtering based on the model fields.

    Args:
        modelClass (class): The model class for which parameters are generated.

    Returns:
        list: A list of manual parameters for filtering based on model fields.
    """
    manual_parameters = []

    for field in modelClass._meta.fields:
        field_name = field.name
        field_type = openapi.TYPE_STRING  # You can set appropriate types based on your field types

        parameter = openapi.Parameter(
            field_name,
            openapi.IN_QUERY,
            description=f"{field_name} filter",
            type=field_type,
            required=False,
        )
        manual_parameters.append(parameter)
    # Additional parameters
    manual_parameters.append(openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER, required=True))
    manual_parameters.append(openapi.Parameter('count_per_page', openapi.IN_QUERY, description="count_per_page", type=openapi.TYPE_INTEGER, required=True))
    manual_parameters.append(openapi.Parameter('filter', openapi.IN_QUERY, description="filter", type=openapi.TYPE_STRING, required=False))
    manual_parameters.append(openapi.Parameter('order_by', openapi.IN_QUERY, description="order_by", type=openapi.TYPE_STRING, required=False))
    manual_parameters.append(openapi.Parameter('ignore[]', openapi.IN_QUERY, description="ignore[]", type=openapi.TYPE_STRING, required=False))
    manual_parameters.append(openapi.Parameter('depth', openapi.IN_QUERY, description="depth", type=openapi.TYPE_INTEGER, required=False))

    return manual_parameters
        
def getViewSet(modelClass):
    """
    Returns a viewset class for the given `modelClass`.

    Parameters:
        - `modelClass`: The model class to create a viewset for.

    Returns:
        - `ApiViewSet`: A viewset class that provides CRUD operations for the `modelClass` model.

    Example Usage:
        ```
        viewset = getViewSet(MyModel)
        ```
    """
    # @permission_classes((IsAuthenticatedOrReadOnly,))
    # @authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
    @permission_classes(
    [
        AllowAny,
    ]
    )
    # @authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
    class ApiViewSet(viewsets.ModelViewSet):
        """
        This class represents the API view set for handling API requests.
        """
        queryset = modelClass.objects.all().order_by("-id")
        serializer_class = getSerializer(modelClass)
        @swagger_auto_schema(
            manual_parameters=generate_manual_parameters(modelClass),
        )
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
    
        # Add a custom method for filtering answers by day and difficulty
        if modelClass.__name__ == "Answer":
            @action(detail=False, methods=['GET'])
            def filter_by_day_and_difficulty(self, request):
                # Get the parameters from the request
                day = request.GET.get("day")
                difficulty = request.GET.get("difficulty")

                # Filter the answers based on day and difficulty
                filtered_answers = Answer.objects.filter(
                    writing_content__day=day,
                    writing_content__difficulty__name=difficulty,
                )

                # Serialize the filtered answers and return as JSON response
                serializer = getSerializer(Answer)
                serialized_data = serializer(filtered_answers, many=True).data
                return Response(serialized_data, status=status.HTTP_200_OK)

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