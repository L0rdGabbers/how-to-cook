# Generated by Django 3.2.20 on 2023-09-08 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
