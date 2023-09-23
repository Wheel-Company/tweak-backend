import json
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from api.models import Category, Difficulty, GrammarContent
import pandas as pd

class Command(BaseCommand):
    help = 'Import grammar_content from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
        parser.add_argument('--db', action='store_true', help='Save data to the database')

    def handle(self, *args, **kwargs):
        errors = []  # List to collect error messages
        save_to_json = kwargs['json']
        save_to_db = kwargs['db']

        if not (save_to_json or save_to_db):
            raise CommandError("No action specified, add --json or --db")

        df = pd.read_excel('./api/management/commands/grammar_content.xlsx')
        data_list = []

        for i, row in df.iterrows():
            try:
                major_category = Category.objects.get(name=row['대분류'], level=1)
                sub_category = Category.objects.get(name=row['중분류'], parent=major_category, level=2)
                detailed_category = Category.objects.get(name=row['소분류'], parent=sub_category, level=3)
                difficulty = Difficulty.objects.get(name=row['난이도'])
            except Category.DoesNotExist:
                errors.append(f"Row {i}: Category does not exist.")
            except Difficulty.DoesNotExist:
                errors.append(f"Row {i}: Difficulty does not exist.")

        if errors:
            for error in errors:
                self.stdout.write(self.style.ERROR(error))
            return  # Exit if there are errors

        # The following block will only run if there were no errors
        for i, row in df.iterrows():
            content_text = {
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

            sequence = (i % 10) + 1

            data = {
                "category": detailed_category.id,
                "difficulty": difficulty.id,
                "day": row['Day'],
                "sequence": sequence,
                "content_text_en": row['en'],
                "content_text": content_text
            }

            data_list.append(data)

            if save_to_db:
                with transaction.atomic():
                    grammar_content = GrammarContent(
                        category=detailed_category,
                        difficulty=difficulty,
                        day=row['Day'],
                        sequence=sequence,
                        content_text_en=row['en'],
                        content_text=content_text
                    )
                    grammar_content.save()

        if save_to_json:
            with open('grammar_content.json', 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully imported grammar_content'))
