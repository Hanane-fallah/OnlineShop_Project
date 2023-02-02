from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import expiry_date_validate, Customer


# VALIDATORS
def digit_validate(digit):
    if digit <= 0:
        raise ValidationError(
            _('must be positive')
        )


# MODELS
class Category(models.Model):
    parent_cat = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=50)
    info = models.TextField(max_length=300)
    price = models.FloatField(validators=[digit_validate])
    qty = models.IntegerField(validators=[digit_validate])
    image = models.ImageField(upload_to='img/product')

    def __str__(self):
        return f'{self.name} : {self.qty}'


class PromotionType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type_id = models.ForeignKey(PromotionType, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    hint = models.CharField(max_length=50)
    # in percentage -> maximum promotion & in cash -> minimum & in cart promo -> Discount phrase
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=False, validators=[expiry_date_validate])

    def __str__(self):
        return f'{self.name} : {self.value}'


class InProcessPromo(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    in_process = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.promotion_id} - {self.product_id}'


class Review(models.Model):
    RATING = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING)
    comment = models.TextField(max_length=600)

    def __str__(self):
        return f'* {self.rating} * : {self.comment}'