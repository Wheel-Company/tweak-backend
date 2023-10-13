import json
from django.core.management.base import BaseCommand, CommandError
from api.models import Difficulty
import pandas as pd

class Command(BaseCommand):
    help = 'Import difficulty levels from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
        parser.add_argument('--db', action='store_true', help='Save data to the database')

    def handle(self, *args, **kwargs):
        save_to_json = kwargs['json']
        save_to_db = kwargs['db']

        if not (save_to_json or save_to_db):
            raise CommandError("No action specified, add --json or --db")

        df = pd.read_excel('./api/management/commands/__contents/difficulty.xlsx')  # Replace with the actual file path
        difficulties = df['난이도'].unique().tolist()  # Assuming the column name is '난이도'

        data_list = []

        for difficulty in difficulties:
            data = {
                "name": difficulty,
            }

            if save_to_db:
                Difficulty.objects.get_or_create(name=difficulty)

            data_list.append(data)

        if save_to_json:
            with open('difficulties.json', 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully imported difficulty levels'))
