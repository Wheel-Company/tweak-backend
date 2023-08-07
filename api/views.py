from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User, Profile, ConnectedAccount, Category, Question, Answer, Subscription, Coupon, Note,Difficulty
from .serializers import UserSerializer, ProfileSerializer, ConnectedAccountSerializer, CategorySerializer, DifficultySerializer,QuestionSerializer, AnswerSerializer, SubscriptionSerializer, CouponSerializer, NoteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def add_account(self, request, pk=None):
        user = self.get_object()
        account_type = request.data.get('account_type')
        account_email = request.data.get('account_email')

        if account_type and account_email:
            account = ConnectedAccount.connect_account(user, account_type, account_email)
            return Response(ConnectedAccountSerializer(account).data, status=status.HTTP_201_CREATED)

        return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ConnectedAccountViewSet(viewsets.ModelViewSet):
    queryset = ConnectedAccount.objects.all()
    serializer_class = ConnectedAccountSerializer

    @action(detail=True, methods=['delete'])
    def disconnect_account(self, request, pk=None):
        account = self.get_object()
        try:
            account.disconnect_account()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned categories,
        by filtering against a `level` query parameter in the URL.
        """
        queryset = Category.objects.all()
        level = self.request.query_params.get('level', None)
        parent = self.request.query_params.get('parent', None)
        category_id = self.request.query_params.get('id', None)
        
        if category_id is not None:
            queryset = queryset.filter(id=category_id)
        elif level is not None:
            queryset = queryset.filter(level=level)
        elif parent is not None:
            queryset = queryset.filter(parent=parent)
        return queryset


class DifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer
    
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        category_id = self.request.query_params.get('category', None)
        day = self.request.query_params.get('day', None)
        difficulty_id = self.request.query_params.get('difficulty', None)

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        if day is not None:
            queryset = queryset.filter(day=day)
        if difficulty_id is not None:
            difficulty = get_object_or_404(Difficulty, id=difficulty_id)
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
