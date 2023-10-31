import json
import os
import datetime
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from api.models import Category, Difficulty, WritingContent

class Command(BaseCommand):
    help = 'Import writing_content from Excel or JSON files'

    def add_arguments(self, parser):
        parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
        parser.add_argument('--db', type=str, help='Save data to the database from a specific JSON file')

    def handle(self, *args, **kwargs):
        start_time = datetime.datetime.now()
        self.stdout.write(f"Script started at {start_time}")

        save_to_json = kwargs['json']
        json_file_name = kwargs['db']
        processed_count = 0

        if not (save_to_json or json_file_name):
            raise CommandError("No action specified, add --json or --db=<json_file_name>")

        if json_file_name:
            json_path = f'./api/management/commands/__contents/json/{json_file_name}.json'
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)

                with transaction.atomic():
                    for data in data_list:
                        category_code = data.pop('category', None)
                        difficulty_id = data.pop('difficulty', None)

                        # Retrieve or create Category and Difficulty instances
                        category = Category.objects.get(code=category_code)
                        difficulty = Difficulty.objects.get(id=difficulty_id)

                        # Create WritingContent instance
                        writing_content = WritingContent(
                            category=category,
                            difficulty=difficulty,
                            **data
                        )
                        writing_content.save()

                self.stdout.write(f"Data from {json_file_name}.json has been saved to the database.")
            else:
                self.stdout.write(f"{json_file_name}.json does not exist.")

        # Existing code for handling Excel files can remain here

        end_time = datetime.datetime.now()
        self.stdout.write(f"Script ended at {end_time}")
        self.stdout.write(f"Total time taken: {end_time - start_time}")
