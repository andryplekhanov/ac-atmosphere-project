from django.contrib import admin
from django.db import models

from app_settings.exchange_rate_parser import get_exchange_rate


class SingletonModel(models.Model):
    """
    Модель данных, которая всегда будет содержать только один объект, то есть только одну запись.
    Даёт возможность использовать информацию из этой модели прямо в шаблоне, без загрузки настроек сайта во view.
    Подробнее: https://evileg.com/ru/post/576/
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Модель автоматически сохраняет все остальные при сохранении объекта,
        что позволяет всегда сохранять в базе только один экземпляр этой модели.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Берет из БД единственный объект настроек.
        Если объекта в БД нет, возвращает новый экземпляр этой модели, который нужно будет потом сохранить.
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class CompanySettings(SingletonModel):
    company = models.CharField(max_length=55, null=True, blank=True, verbose_name='название компании')
    description = models.TextField(null=True, blank=True, verbose_name='краткое описание')
    email = models.EmailField('email', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='номер телефона для связи')
    phone_messengers = models.CharField(max_length=20, null=True, blank=True, verbose_name='номер телефона (мессенджеры)')

    def __str__(self):
        return str(f'компания {self.company}')

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компания'


class CurrencySettings(SingletonModel):
    use_fix_exchange_rate = models.BooleanField(default=False, verbose_name='использовать фиксированный курс доллара')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                        verbose_name='курс доллара', db_index=True)

    @property
    @admin.display(description='текущий курс')
    def dollar_exchange_rate(self):
        if self.use_fix_exchange_rate:
            return self.exchange_rate
        return get_exchange_rate()

    def __str__(self):
        return str(f'{self.dollar_exchange_rate}')

    class Meta:
        verbose_name = 'настройка валюты'
        verbose_name_plural = 'настройки валюты'


class AdminsSettings(SingletonModel):
    pass

    def __str__(self):
        return str(f'настройки администраторов')

    class Meta:
        verbose_name = 'настройка администраторов'
        verbose_name_plural = 'настройки администраторов'


class AdminItem(SingletonModel):
    admins_settings = models.ForeignKey('AdminsSettings', related_name='admin_item', on_delete=models.CASCADE,
                                        verbose_name='настройки администраторов')
    name = models.CharField(max_length=85, verbose_name='имя')
    phone_number = models.CharField(max_length=20, verbose_name='номер телефона')
    tg_id = models.BigIntegerField(unique=True, db_index=True, verbose_name='id Telegram')
    username = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name='username Telegram')

    def __str__(self):
        return str(f'{self.name}')

    class Meta:
        verbose_name = 'настройка администратора'
        verbose_name_plural = 'настройки администратора'
