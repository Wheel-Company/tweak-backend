from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    is_email_registered = models.BooleanField(default=False)


class ConnectedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20)  # e.g. 'google', 'apple', 'email'
    account_email = models.EmailField()

    def disconnect_account(self):
        if self.user.connectedaccount_set.count() > 1:
            self.delete()
        else:
            raise ValueError("Cannot disconnect the only connected account.")

    @classmethod
    def connect_account(cls, user, account_type, account_email):
        return cls.objects.create(user=user, account_type=account_type, account_email=account_email)


# 카테고리 모델: 문제의 카테고리 정보를 저장
class Category(models.Model):
    name = models.CharField(max_length=100)  # 카테고리 이름
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # 부모 카테고리를 참조
    level = models.IntegerField(default=1)  # 카테고리의 레벨 (1 for major category, 2 for sub-category, 3 for sub-sub-category)

class Difficulty(models.Model):
    name = models.CharField(max_length=100, default ='Beginner')  # 난이도 이름
    
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 문제의 카테고리를 참조
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, null=True)  # 문제의 난이도를 참조, NULL 허용
    day = models.IntegerField(default=1)  # 문제의 Day (기본값 1로 설정)
    question_text_en = models.TextField(null=True)  # 문제 텍스트 (영어)
    question_text_ko = models.TextField(null=True)  # 문제 텍스트 (한국어)


# 답변 모델: 사용자의 답변 정보를 저장
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 인스턴스를 참조
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 답변의 질문을 참조
    user_answer_text = models.TextField()  # 사용자 답변 텍스트
    is_correct = models.BooleanField(default=False)  # 답변이 정답인지 여부 (문법 문제의 답변인 경우에만 사용)
    answered_at = models.DateTimeField(auto_now_add=True)


# 구독 모델: 사용자의 구독 정보를 저장
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 인스턴스를 참조
    start_date = models.DateField()  # 구독 시작 날짜
    end_date = models.DateField()  # 구독 종료 날짜

# 쿠폰 모델: 사용자의 쿠폰 정보를 저장
class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 인스턴스를 참조
    code = models.CharField(max_length=100)  # 쿠폰 코드
    is_used = models.BooleanField(default=False)  # 쿠폰 사용 여부

# 노트 모델: 사용자의 노트 정보를 저장
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 인스턴스를 참조
    content = models.TextField()  # 노트 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 노트 생성 시각
