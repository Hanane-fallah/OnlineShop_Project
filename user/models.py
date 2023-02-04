from datetime import date
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from iranian_cities.fields import OstanField, ShahrestanField


# VALIDATORS
def age_validate(age):
    if 18 < age:
        if age < 100:
            return True
        else:
            raise ValidationError(
                _('Age in invalid')
            )
    else:
        raise ValidationError(
            _('Age must be more than 18')
        )


def account_number_validate(num):
    if len(str(num)) != 16:
        raise ValidationError(
            _('Account number is invalid')
        )


def expiry_date_validate(ex_date):
    today = date.today()
    if ex_date < today:
        raise ValidationError(
            _('Expire Date is invalid')
        )


# MODELS
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(validators=[age_validate], blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True,
                              validators=[RegexValidator(r'09\d{9}', 'Your mobile number must start with 09')])
    slug = models.SlugField(blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.user_name)
        super().save()

    def __str__(self):
        return self.user_name


class Address(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ostan = OstanField(default=8)
    shahrestan = ShahrestanField(default=126)
    street = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=9)
    detail = models.TextField(max_length=300)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ostan} - {self.shahrestan} - {self.detail[:10]}'


class PayAccount(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.BigIntegerField(validators=[account_number_validate])
    expiry_date = models.DateField(validators=[expiry_date_validate])
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.account_number} : {self.is_default}'
