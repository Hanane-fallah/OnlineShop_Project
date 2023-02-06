from datetime import date
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from iranian_cities.fields import OstanField, ShahrestanField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin


# VALIDATORS
def age_validate(age) -> None:
    """
    return True if age value is in valid range (18-100)
    else raise validation-error
    :param age:user age
    :return:True
    """
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
    """
    check account-number's length
    raise ValidationError if != 16
    :param num: account number
    :return: None
    """
    if len(str(num)) != 16:
        raise ValidationError(
            _('Account number is invalid')
        )


def expiry_date_validate(ex_date):
    """
    check expiry date
    :raise ValidationError if expiry-date is passed from current day
    :param ex_date: entered expiry date
    :return: None
    """
    today = date.today()
    if ex_date < today:
        raise ValidationError(
            _('Expire Date is invalid')
        )


# MODELS
class User(AbstractUser):
    """
    define User model overriding on django AbstractUser model

    ...

    Additional Attributes
    ----------
    age : int
        age of the person
    mobile : str
        mobile number of the person
    slug : str
        a short label for person's username

    Methods
    -------
    save:
        set the slug field and save the object in database
    str:
        string representation of User object.
    """
    age = models.IntegerField(validators=[age_validate], blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True,
                              validators=[RegexValidator(r'09\d{9}', 'Your mobile number must start with 09')])
    slug = models.SlugField(blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        adding a slug (-) in each of the string where there is a space in username
        & put it in slug field
        & then save the object in database
        :param force_insert, force_update, using, update_fields: django default params
        :return:None
        """
        self.slug = slugify(self.username)
        super().save()

    def __str__(self):
        return self.username


class Address(models.Model):
    """
    define Address model for customers

    ...

    Attributes
    ----------
    user_id : user object
        foreign key to user model ( to define address owner )
    ostan : iranian_cities.models.Ostan
        ostan of address
    shahrestan : iranian_cities.models.shahrestan
        shahrestan of address
    street : str
        street of address
    postal_code : str
        postal_code of address
    detail : str
        some extra info about address like apartment floor ...
    is_default : bool
        True if user's default address, otherwise False
    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Address object.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ostan = OstanField(default=8)
    shahrestan = ShahrestanField(default=126)
    street = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=9)
    detail = models.TextField(max_length=300)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ostan} - {self.shahrestan} - {self.detail[:10]}'


class PayAccount(models.Model):
    """
    define Pay-Account model for customers

    ...

    Attributes
    ----------
    user_id : user object
        foreign key to user model ( to define account owner )
    account_number : int
        user's account number
    expiry_date : date
        account's expiry date
    is_default : bool
        True if user's default account, otherwise False
    Methods
    -------
    save:
        save the object in database
    str:
        string representation of PayAccount object.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.BigIntegerField(validators=[account_number_validate])
    expiry_date = models.DateField(validators=[expiry_date_validate])
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.account_number} : {self.is_default}'
