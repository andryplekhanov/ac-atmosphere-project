from decimal import Decimal

from django.contrib import admin
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app_products.validators import image_size_validate
from app_settings.models import CurrencySettings

image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'svg'],
        message='Ошибка загрузки: допускаются только файлы с расширением .jpg .jpeg .gif .png .svg'
    )


class Category(MPTTModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='url-адрес')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='родительская категория')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    # def get_absolute_url(self):
    #     return reverse('good-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.name


class Product(models.Model):
    AVAILABLE_CHOICES = (
        ("no", "Не доступно"),
        ("stock", "В наличии"),
        ("order", "Под заказ"),
    )

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, related_name='category',
                              verbose_name='категория', null=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True, verbose_name='заголовок')
    description = models.TextField(blank=True, verbose_name='описание')
    use_dollars = models.BooleanField(default=True,
                                      verbose_name='использовать цену в долларах (если нет, укажите цену в рублях)')
    price_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       verbose_name='цена в долларах', db_index=True)
    price_rub = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                    verbose_name='цена в рублях', db_index=True)
    available = models.CharField(max_length=30, choices=AVAILABLE_CHOICES, verbose_name='наличие', default="stock")
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'товар / услуга'
        verbose_name_plural = 'товары / услуги'

    def __str__(self):
        return f"id: {self.id}, {self.title}"

    @property
    @admin.display(description='цена (руб)')
    def total_price(self):
        if self.use_dollars:
            dollar_settings = CurrencySettings.objects.all().first()
            dollar_price = self.price_dollar if self.price_dollar else Decimal.from_float(0.0)
            total_cost = dollar_price * dollar_settings.dollar_exchange_rate
            return total_cost.quantize(Decimal("1.00"))
        else:
            return self.price_rub if self.price_rub else Decimal.from_float(0.0)


class Image(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='изображение',
                              validators=[image_validator, image_size_validate])
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', verbose_name='продукт')

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
