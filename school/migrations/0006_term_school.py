# Generated by Django 3.2.10 on 2022-05-23 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_administrator_is_verified_and_more'),
        ('school', '0005_auto_20220522_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.school'),
            preserve_default=False,
        ),
    ]
