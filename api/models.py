from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)  # 마지막 로그인 시간
    sns_type = models.CharField(max_length=30, null=True, blank=True)
    sns_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 마지막 로그인 시간

LEVEL_CHOICES = [
    (1, '대분류'),
    (2, '중분류'),
    (3, '소분류'),
]
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    code = models.CharField(max_length=6, unique=True, null=True, blank=True)

class Difficulty(models.Model):
    name = models.CharField(max_length=100, default='Beginner')

class WritingContent(models.Model):
    content_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, null=True)
    day = models.IntegerField(default=1)
    sequence = models.IntegerField(default=1)  # 문제 순서
    content_text_en = models.TextField(blank=True)
    content_text = models.JSONField(null=True)

    class Meta:
        db_table = 'api_writing_content'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    writing_content = models.ForeignKey(WritingContent, on_delete=models.CASCADE)
    user_answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)


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

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)  # 예: '문제 풀이', '로그인', '신고'
    activity_detail = models.TextField(null=True, blank=True)  # 활동의 세부 정보
    activity_date = models.DateTimeField(auto_now_add=True)

REPORT_TYPE_CHOICES = [
    ('contens', '문제이상'),
    ('answer', '답변이상'),
]

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_id = models.ForeignKey(WritingContent, on_delete=models.CASCADE)
    reason = models.TextField()  # 신고 이유
    language = models.CharField(max_length=10)  # 언어 설정
    report_type = models.CharField(choices=REPORT_TYPE_CHOICES, max_length=50, unique=True, null=True, blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)  # 신고 시간

class SavedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_text = models.ForeignKey(WritingContent, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)  # 저장 시간

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=100)  # 구독 종류 (예: '월간', '연간')
    price = models.DecimalField(default=False,max_digits=10, decimal_places=2,null=True, blank=True)  # 가격
    description = models.TextField(default=False,null=True, blank=True)  # 설명
    created_at = models.DateTimeField(auto_now_add=True)  # 구독 시작 시간
