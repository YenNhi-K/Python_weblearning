# Generated by Django 5.0.6 on 2024-05-17 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english_test', '0002_remove_test_number_of_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='number_of_words',
            field=models.IntegerField(default=0),
        ),
    ]
