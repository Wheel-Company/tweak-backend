# Generated by Django 4.2.3 on 2023-08-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_grammarquestion_category_level_profile_nickname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_email_registered',
            field=models.BooleanField(default=False),
        ),
    ]