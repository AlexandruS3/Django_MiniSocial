# Generated by Django 4.2.2 on 2023-07-30 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_social', '0003_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(to='mini_social.customuser'),
        ),
    ]