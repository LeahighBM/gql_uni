# Generated by Django 5.2.4 on 2025-07-24 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni_app', '0002_alter_student_gpa_alter_student_major'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uni_app.course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uni_app.student')),
            ],
        ),
    ]
