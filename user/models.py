from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

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

# MODELS
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
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


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Address(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=9)
    detail = models.TextField(max_length=300)
    is_default = models.BooleanField()

    def __str__(self):
        return f'{self.street} - {self.detail[10]} : {self.is_default}'
