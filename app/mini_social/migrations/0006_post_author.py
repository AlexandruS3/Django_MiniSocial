# Generated by Django 4.2.2 on 2023-08-04 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mini_social', '0005_customuser_session_data_backup'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mini_social.customuser'),
        ),
    ]