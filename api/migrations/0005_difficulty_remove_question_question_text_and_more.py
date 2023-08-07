# Generated by Django 4.2.3 on 2023-08-04 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_usergrammarquestion_grammar_question_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Beginner', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.AddField(
            model_name='question',
            name='day',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text_ko',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.difficulty'),
        ),
    ]
