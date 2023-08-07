from rest_framework import serializers
from .models import User, Profile, ConnectedAccount, Category, Difficulty,Question, Answer, Subscription, Coupon, Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']  # or whatever fields you want

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ConnectedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedAccount
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    difficulty = DifficultySerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'category', 'difficulty', 'day', 'question_text_en', 'question_text_ko']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'