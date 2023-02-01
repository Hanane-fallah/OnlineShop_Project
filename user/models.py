from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


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
