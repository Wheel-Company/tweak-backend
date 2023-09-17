from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    is_email_registered = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.IntegerField(default=1)

class Difficulty(models.Model):
    name = models.CharField(max_length=100, default='Beginner')

class GrammarContent(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, null=True)
    day = models.IntegerField(default=1)
    sequence = models.IntegerField(default=1)  # 문제 순서
    question_text_en = models.TextField(blank=True)
    question_text = models.JSONField(null=True)

    class Meta:
        db_table = 'api_grammar_content'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grammar_content = models.ForeignKey(GrammarContent, on_delete=models.CASCADE)
    user_answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=100, blank=True)  # 구독 종류

class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)  # 쿠폰 만료 날짜

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Banner(models.Model):
    image_url = models.URLField()
    language = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    sequence = models.PositiveIntegerField()
