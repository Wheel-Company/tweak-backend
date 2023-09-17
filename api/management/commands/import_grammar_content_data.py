from django.core.management.base import BaseCommand
from api.models import Category, Difficulty, GrammarContent
import pandas as pd

class Command(BaseCommand):
    help = 'Import grammar_content from an Excel file'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('./api/management/commands/grammar_content.xlsx')

        for i, row in df.iterrows():
            # try:
            major_category = Category.objects.get(name=row['대분류'], level=1)
            sub_category = Category.objects.get(name=row['중분류'], parent=major_category, level=2)
            detailed_category = Category.objects.get(name=row['소분류'], parent=sub_category, level=3)
            difficulty = Difficulty.objects.get(name=row['난이도'])
            # except Category.DoesNotExist:
            #     print(f"Row {i}: Category does not exist.")
            #     continue
            # except Difficulty.DoesNotExist:
            #     print(f"Row {i}: Difficulty does not exist.")
            #     continue

            question_text = {
                'ko': row['ko'],
                'es': row['es'],
                'fr': row['fr'],
                'it': row['it'],
                'ja': row['ja'],
                'pt': row['pt'],
                'de': row['de'],
                'ru': row['ru'],
                'id': row['id'],
                'tr': row['tr'],
                'hi': row['hi'],
                'ar': row['ar'],
                'pl': row['pl'],
                'ms': row['ms'],
                'uk': row['uk'],
                'ro': row['ro'],
                'vi': row['vi'],
            }

            # sequence 값을 설정 (예: 1~10)
            sequence = (i % 10) + 1

            grammar_content = GrammarContent(
                category=detailed_category,
                difficulty=difficulty,
                day=row['Day'],
                sequence=sequence,  # sequence 필드 추가
                question_text_en=row['en'],
                question_text=question_text
            )
            grammar_content.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported grammar_content'))

