# Generated by Django 5.0.4 on 2024-04-20 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('userType', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='LabTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionNumber', models.CharField(max_length=30)),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.coursetable')),
                ('taId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.usertable')),
            ],
        ),
        migrations.AddField(
            model_name='coursetable',
            name='instructorId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduler.usertable'),
        ),
    ]
