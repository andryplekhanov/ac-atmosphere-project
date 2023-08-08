# Generated by Django 4.2.4 on 2023-08-08 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_fix_exchange_rate', models.BooleanField(default=False, verbose_name='использовать фиксированный курс доллара')),
                ('exchange_rate', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=10, null=True, verbose_name='курс доллара')),
            ],
            options={
                'verbose_name': 'настройка валюты',
                'verbose_name_plural': 'настройки валюты',
            },
        ),
    ]
