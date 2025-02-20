# Generated by Django 2.1.5 on 2019-08-28 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_auto_20190828_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=6)),
                ('exam_grade', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AlterField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='classes.Classroom'),
        ),
    ]
