import json
from django.core.management.base import BaseCommand, CommandError
from api.models import Category  # Replace with your actual app and model name
import pandas as pd


class Command(BaseCommand):
    help = 'Import categories from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
        parser.add_argument('--db', action='store_true', help='Save data to the database')

    def handle(self, *args, **kwargs):
        save_to_json = kwargs['json']
        save_to_db = kwargs['db']

        if not (save_to_json or save_to_db):
            raise CommandError("No action specified, add --json or --db")

        df = pd.read_excel('./api/management/commands/tweak_category.xlsx')  # Replace with your actual file path

        last_category = {1: None, 2: None}
        data_list = []

        for idx, row in df.iterrows():
            main_category_name = row['대분류']
            sub_category_name = row['중분류']
            detailed_category_name = row['소분류']

            main_category, sub_category, detailed_category = None, None, None

            if save_to_db:
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

            data = {
                'id': detailed_category.id if detailed_category else None,
                'name': detailed_category_name,
                'level': 3,
                'parent': sub_category.id if sub_category else None
            }

            data_list.append(data)

        if save_to_json:
            json_data = {
                'responseCode': 200,
                'responseMsg': 'OK',
                'result': data_list
            }

            with open('categories.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories'))