# Generated by Django 5.2.1 on 2025-05-26 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_usersmod_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswersmod',
            name='direction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.directionmod', verbose_name="Yo'nalishi"),
        ),
        migrations.AddField(
            model_name='useranswersmod',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.teachersmod', verbose_name="O'qituvchi"),
        ),
    ]
