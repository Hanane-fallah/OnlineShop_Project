from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import expiry_date_validate


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
    hint = models.CharField(max_length=50)  # in percentage -> maximum promotion & in cart promo -> Discount phrase
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=False, validators=[expiry_date_validate])

    def __str__(self):
        return f'{self.name} : {self.value}'