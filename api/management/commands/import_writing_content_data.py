import json
import os
import datetime  # Import the datetime module
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from api.models import Category, Difficulty, WritingContent
import pandas as pd

class Command(BaseCommand):
    help = 'Import writing_content from Excel files'

    def add_arguments(self, parser):
        parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
        parser.add_argument('--db', action='store_true', help='Save data to the database')

    def handle(self, *args, **kwargs):
        start_time = datetime.datetime.now()  # Record the start time
        self.stdout.write(f"Script started at {start_time}")

        save_to_json = kwargs['json']
        save_to_db = kwargs['db']
        processed_count = 0

        if not (save_to_json or save_to_db):
            raise CommandError("No action specified, add --json or --db")

        excel_files = os.listdir('./api/management/commands/__contents/write_contents')

        for excel_file in excel_files:
            file_start_time = datetime.datetime.now()  # Record the start time for this file
            self.stdout.write(f"Started processing {excel_file} at {file_start_time}")

            json_file_name = excel_file.replace('.xlsx', '.json')
            json_path = f'./api/management/commands/__contents/write_contents/{json_file_name}'

            if excel_file.endswith('.xlsx') and not os.path.exists(json_path):
                data_list = []
                errors = []

                with transaction.atomic():
                    df_start_time = datetime.datetime.now()  # Record the start time for reading the Excel file
                    df = pd.read_excel(f'./api/management/commands/__contents/write_contents/{excel_file}')
                    df_end_time = datetime.datetime.now()  # Record the end time for reading the Excel file
                    self.stdout.write(f"Time taken to read Excel: {df_end_time - df_start_time}")


                    for i, row in df.iterrows():
                        try:
                            major_category = Category.objects.get(name=row['대분류'], level=1)
                            print("Full major_category object:", major_category.__dict__)
                            print(f"major_category: {major_category.id}, {major_category.name}")
                            print("major_category", major_category)
                            print("sub_category", sub_category)
                            print("detailed_category", detailed_category)
                            sub_category = Category.objects.get(name=row['중분류'], parent=major_category, level=2)
                            detailed_category = Category.objects.get(name=row['소분류'], parent=sub_category, level=3)
                            difficulty = Difficulty.objects.get(name=row['난이도'])
                        except Category.DoesNotExist as e:
                            errors.append(f"Row {i}: Category does not exist.")
                            self.stdout.write(f"Error on row {i}, column '대분류': {e}")
                            self.stdout.write(f"Row details: {row.to_dict()}")  # Log the entire row
                            continue
                        except Difficulty.DoesNotExist as e:
                            errors.append(f"Row {i}: Difficulty does not exist.")
                            self.stdout.write(f"Error on row {i}, column '난이도': {e}")
                            continue
                        except Exception as e:  # Capture any other exception
                            errors.append(f"Row {i}: An unexpected error occurred.")
                            self.stdout.write(f"Unexpected error on row {i}: {e}")
                            continue

                        content_text = {lang: row[lang] for lang in ['ko', 'es', 'fr', 'it', 'ja', 'pt', 'de', 'ru', 'id', 'tr', 'hi', 'ar', 'pl', 'ms', 'uk', 'ro', 'vi']}

                        sequence = str((i % 10) + 1)
                        day = str(row['Day'])
                        content_code = f"{detailed_category.code}{difficulty.id}{day}{sequence}"

                        data = {
                            "content_code": content_code,
                            "category": detailed_category.code,
                            "difficulty": difficulty.id,
                            "day": row['Day'],
                            "sequence": int(sequence),
                            "content_text_en": row['en'],
                            "content_text": content_text
                        }

                        if save_to_db:
                            writing_content = WritingContent(
                                content_code=content_code,
                                category=detailed_category,
                                difficulty=difficulty,
                                day=row['Day'],
                                sequence=int(sequence),
                                content_text_en=row['en'],
                                content_text=content_text
                            )
                            writing_content.save()
                            data['id'] = writing_content.id  # Update the id after saving to DB

                        data_list.append(data)

                    if save_to_json and not errors:
                        json_start_time = datetime.datetime.now()  # Record the start time for saving the JSON file
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(data_list, f, ensure_ascii=False, indent=4)
                        json_end_time = datetime.datetime.now()  # Record the end time for saving the JSON file
                        self.stdout.write(f"Time taken to save JSON: {json_end_time - json_start_time}")

                file_end_time = datetime.datetime.now()  # Record the end time for this file
                self.stdout.write(f"Finished processing {excel_file} at {file_end_time}")
                self.stdout.write(f"Time taken for this file: {file_end_time - file_start_time}")

        end_time = datetime.datetime.now()  # Record the end time
        self.stdout.write(f"Script ended at {end_time}")
        self.stdout.write(f"Total time taken: {end_time - start_time}")
