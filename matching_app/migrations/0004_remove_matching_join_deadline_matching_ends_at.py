# Generated by Django 4.2 on 2023-04-27 19:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matching_app', '0003_matching_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matching',
            name='join_deadline',
        ),
        migrations.AddField(
            model_name='matching',
            name='ends_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='모임 종료 일시'),
            preserve_default=False,
        ),
    ]
