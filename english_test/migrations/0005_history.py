# Generated by Django 5.0.6 on 2024-05-21 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english_test', '0004_test_topic'),
        ('user', '0002_alter_user_user_id_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.IntegerField(default=0)),
                ('number_of_questions', models.IntegerField(default=0)),
                ('type', models.BooleanField(default=False)),
                ('test_time', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='english_test.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
