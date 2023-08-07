from django.core.management.base import BaseCommand
from api.models import Category  # 이 부분은 실제 앱 이름과 모델 이름에 맞게 변경해야 합니다.
import pandas as pd


class Command(BaseCommand):
    help = 'Import categories from a Excel file'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('./api/management/commands/tweak_category.xlsx')  # 실제 파일 경로로 변경해야 합니다.

        last_category = {1: None, 2: None}

        for idx, row in df.iterrows():
            main_category_name = row['대분류']
            sub_category_name = row['중분류']
            detailed_category_name = row['소분류']

            if last_category[1] is None or last_category[1].name != main_category_name:
                main_category = Category(name=main_category_name, level=1)
                main_category.save()
                last_category[1] = main_category
            else:
                main_category = last_category[1]

            if last_category[2] is None or last_category[2].name != sub_category_name:
                sub_category = Category(name=sub_category_name, parent=main_category, level=2)
                sub_category.save()
                last_category[2] = sub_category
            else:
                sub_category = last_category[2]

            detailed_category = Category(name=detailed_category_name, parent=sub_category, level=3)
            detailed_category.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully imported categories'))
