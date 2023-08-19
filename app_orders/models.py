from decimal import Decimal

from django.contrib import admin
from django.db import models

from app_products.models import Product
from app_telegram.models import TGUser, TimeBasedModel


class Order(TimeBasedModel):
    STATUS_CHOICES = (
        ("finished", "Завершён"),
        ("new", "Новый"),
        ("progress", "В работе"),
        ("canceled", "Отменён"),
    )
    DELIVERY_CHOICES = (
        ("self", "Самовывоз"),
        ("delivery", "Доставка"),
    )

    user = models.ForeignKey(TGUser, on_delete=models.SET_NULL, null=True, verbose_name='пользователь',
                             related_name='orders')
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                   verbose_name='скидка в рублях')
    delivery_type = models.CharField(max_length=30, choices=DELIVERY_CHOICES, verbose_name='доставка',
                                     default="delivery")
    address = models.CharField(max_length=255, verbose_name='адрес')
    paid = models.BooleanField(default=False, verbose_name='оплачен')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='статус', default="new")
    comment = models.TextField(null=True, blank=True, max_length=10000, verbose_name='комментарий администратора')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'order #{self.id}'

    @property
    @admin.display(description='итоговая стоимость')
    def get_total_cost(self):
        discount = self.discount if self.discount else 0
        total_cost = float(sum(item.get_cost() for item in self.items.all()) - discount)
        return Decimal.from_float(total_cost).quantize(Decimal("1.00"))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.product}'

    def get_cost(self):
        total_cost = float(self.price * self.quantity)
        return Decimal.from_float(total_cost).quantize(Decimal("1.00"))
