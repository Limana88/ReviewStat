# Generated by Django 4.2.1 on 2023-05-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyze',
            name='name_company',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
