from django.db import models
from decimal import Decimal
from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_("Имя"), max_length=50)
    last_name = models.CharField(_("Фамилия"), max_length=50)
    email = models.EmailField(_("Email"))
    address = models.CharField(_("Адрес"), max_length=250)
    postal_code = models.CharField(_("Почтовый индекс"), max_length=20)
    city = models.CharField(_("Город"), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Купон')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Скидка (%)')


    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost_before_discount(self):
        """Возвращает общую стоимость товаров до применения скидки."""
        return sum(item.get_cost() for item in self.items.all())

    def get_discount_amount(self):
        """Возвращает сумму скидки в денежном выражении."""
        if self.discount > 0:
            return self.get_total_cost_before_discount() * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """Возвращает итоговую стоимость заказа после вычета скидки."""
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount_amount()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity