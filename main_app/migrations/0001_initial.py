# Generated by Django 5.2.1 on 2025-05-23 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DirectionMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('name', models.CharField(max_length=20, verbose_name="Yo'nalishlar")),
            ],
            options={
                'verbose_name': "Yo'nalish",
                'verbose_name_plural': "Yo'nalishlar",
            },
        ),
        migrations.CreateModel(
            name='QuestionMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('question', models.TextField(verbose_name='Savollar')),
                ('answer_A', models.CharField(max_length=255, verbose_name='A Javob')),
                ('answer_B', models.CharField(max_length=255, verbose_name='B Javob')),
                ('answer_C', models.CharField(max_length=255, verbose_name='c Javob')),
                ('answer_D', models.CharField(max_length=255, verbose_name='D Javob')),
            ],
            options={
                'verbose_name': 'Savol',
                'verbose_name_plural': 'Savollar',
            },
        ),
        migrations.CreateModel(
            name='RewardsMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('amount', models.IntegerField(verbose_name='Mukofot summasi')),
            ],
            options={
                'verbose_name': 'Mukofot',
                'verbose_name_plural': 'Mukofot summasi',
            },
        ),
        migrations.CreateModel(
            name='TeachersMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('full_name', models.CharField(max_length=100, verbose_name='Ismi')),
                ('direction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.directionmod', verbose_name="Yo'nalishi")),
            ],
            options={
                'verbose_name': "O'qituvchi",
                'verbose_name_plural': "O'qituvchilar",
            },
        ),
        migrations.CreateModel(
            name='GroupsMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('name', models.CharField(max_length=50, verbose_name='Guruh nomi')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.teachersmod', verbose_name="Guruh o'qituvchisi")),
            ],
            options={
                'verbose_name': 'Guruh',
                'verbose_name_plural': 'Guruhlar',
            },
        ),
        migrations.CreateModel(
            name='UsersMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='Foydlanuvchi ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Ismi')),
                ('start_class_time', models.TimeField(verbose_name='Dasr boshlanish vaqti')),
                ('balance', models.IntegerField(default=0, verbose_name='Hisob')),
                ('created_at', models.DateTimeField(verbose_name='Yaratilgan vaqt')),
                ('direction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.directionmod', verbose_name="Yo'nalishi")),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.teachersmod', verbose_name="O'qituvchi")),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='UserAnswersMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Yaratilgan vaqt')),
                ('answer_A', models.CharField(max_length=255, verbose_name='A Javob')),
                ('answer_B', models.CharField(max_length=255, verbose_name='B Javob')),
                ('answer_C', models.CharField(max_length=255, verbose_name='C Javob')),
                ('answer_D', models.CharField(max_length=255, verbose_name='D Javob')),
                ('answer', models.CharField(choices=[('--', '--'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='--', max_length=255, verbose_name='Tanlagan javobi')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.questionmod', verbose_name='Savol')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.usersmod', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi javobi',
                'verbose_name_plural': 'Foydalanuvchi javoblari',
            },
        ),
    ]
