import json
from django.core.management.base import BaseCommand, CommandError
from api.models import Category  # Replace with your actual app and model name
import pandas as pd

class Command(BaseCommand):
    help = 'Import categories from an Excel file'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('./api/management/commands/contents/tweak_category.xlsx', dtype=str)  # Read all data as str
        data_list = []
        seen = set()

        for idx, row in df.iterrows():
            main_category_id = row['ID']
            main_category_name = row['대분류']
            sub_category_id = row['ID.1']
            sub_category_name = row['중분류']
            detailed_category_id = row['ID.2']
            detailed_category_name = row['소분류']

            categories = [
                {'code': main_category_id, 'name': main_category_name, 'level': 1, 'parent': None},
                {'code': f"{main_category_id}{sub_category_id}", 'name': sub_category_name, 'level': 2, 'parent': main_category_id},
                {'code': f"{main_category_id}{sub_category_id}{detailed_category_id}", 'name': detailed_category_name, 'level': 3, 'parent': f"{main_category_id}{sub_category_id}"}
            ]

            for category in categories:
                cat_code = category['code']
                if cat_code in seen:
                    continue
                seen.add(cat_code)

                cat_obj, _ = Category.objects.get_or_create(
                    code=cat_code,
                    defaults={'name': category['name'], 'level': category['level'], 'parent': Category.objects.filter(code=category['parent']).first() if category['parent'] else None}
                )
                category['id'] = cat_obj.id
                data_list.append(category)

        json_data = {
            'responseCode': 200,
            'responseMsg': 'OK',
            'result': data_list
        }

        with open('categories.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully imported categories'))
