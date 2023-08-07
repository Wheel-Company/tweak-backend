from django.core.management.base import BaseCommand
from api.models import Category, Difficulty, Question
import pandas as pd

class Command(BaseCommand):
    help = 'Import questions from a Excel file'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('./api/management/commands/questions.xlsx')  # 실제 파일 경로로 변경해야 합니다.

        for i, row in df.iterrows():
            try:
                # 대분류, 중분류, 소분류를 찾는 부분
                major_category = Category.objects.get(name=row['대분류'], level=1)
                sub_category = Category.objects.get(name=row['중분류'], parent=major_category, level=2)
                detailed_category = Category.objects.get(name=row['소분류'], parent=sub_category, level=3)
                
                difficulty = Difficulty.objects.get(name=row['난이도'])
                
                # 이후 문제를 생성하고 저장하는 코드...
                
            except Category.DoesNotExist:
                print(f"Row {i}: Category does not exist.")
            except Difficulty.DoesNotExist:
                print(f"Row {i}: Difficulty does not exist.")



            question = Question(
                category=detailed_category,
                difficulty=difficulty,
                day=row['Day'],
                question_text_en=row['en'],
                question_text_ko=row['ko'],
            )
            question.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported questions'))
