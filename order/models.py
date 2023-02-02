import uuid

from django.db import models

from product.models import Promotion, Product
from user.models import Customer, PayAccount


# VALIDATORS

# MODELS
class UserCart(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} : {self.id}'


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.price} $'


class CartStatus(models.Model):
    STATUS = [
        ('verification', 'verification'),
        ('equiping', 'equiping'),
        ('sending', 'sending'),
        ('delivered', 'delivered')
    ]
    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return self.status


class CartDetail(models.Model):
    cart_id = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    order_date = models.DateField(null=True, blank=True)
    pay_account_id = models.ForeignKey(PayAccount, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_id = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    entry = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cart_id} - {self.order_date} : {self.total_amount} $ - {self.entry}'


class CartItem(models.Model):
    cart_id = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return f'{self.product_id} ^ {self.qty}'
