import uuid

from django.db import models

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
    name =  models.CharField(max_length=100, unique=True)
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

# class CartDetail(models.Model):
#     cart_id = models.ForeignKey(UserCart, models.CASCADE)
#     order_date = models.DateField(null=True, blank=True)
#     pay_account_id = models.ForeignKey(PayAccount, on_delete=models.SET_NULL, null=True, blank=True)
#     shipping_id = models.ForeignKey(Shipping)
#