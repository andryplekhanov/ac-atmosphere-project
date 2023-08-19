# Generated by Django 4.2.4 on 2023-08-18 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_telegram', '0010_tguser_is_banned_alter_callrequest_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='скидка в рублях')),
                ('delivery_type', models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='delivery', max_length=30, verbose_name='доставка')),
                ('address', models.CharField(max_length=255, verbose_name='адрес')),
                ('paid', models.BooleanField(default=False, verbose_name='оплачен')),
                ('status', models.CharField(choices=[('finished', 'Завершён'), ('new', 'Новый'), ('progress', 'В работе'), ('canceled', 'Отменён')], default='new', max_length=30, verbose_name='статус')),
                ('comment', models.TextField(blank=True, max_length=10000, null=True, verbose_name='комментарий администратора')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='app_telegram.tguser', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]