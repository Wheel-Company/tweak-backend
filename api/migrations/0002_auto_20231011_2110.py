# Generated by Django 3.2.11 on 2023-10-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sns_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='sns_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
