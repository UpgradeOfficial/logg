# Generated by Django 3.2.10 on 2022-05-16 21:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('payment_provider', models.CharField(blank=True, choices=[('T', 'paystack'), ('F', 'flutterwave')], max_length=20, null=True, verbose_name='Payment Provider')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=30)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
