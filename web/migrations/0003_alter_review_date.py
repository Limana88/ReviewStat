# Generated by Django 4.2.1 on 2023-05-25 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.CharField(),
        ),
    ]